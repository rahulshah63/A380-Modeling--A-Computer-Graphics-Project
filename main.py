# PLease Increase Brightness To MAX Level.

import glfw
from OpenGL.GL import *
import math
import lookAt
import Perspective_projection
import Arithmetic
from Vector3 import Vector3 as v3
import Vector3

from shader import Shader
from loaded_object import LoadedObject
from light import DirLight, PointLight, SpotLight


class Window:
    def __init__(self, width: int, height: int, title: str):
        # Initialize window
        if not glfw.init():
            raise Exception("GLFW cannot be initialized!")

        self._width, self._height = width, height
        self._window = glfw.create_window(width, height, 'AirBUS A380 Modeling', None, None)

        if not self._window:
            glfw.terminate()
            raise Exception("Window cannot be created!")

        # Set resize handler
        glfw.set_window_size_callback(self._window, self._on_resize)
        # Set keyboard input handler
        glfw.set_key_callback(self._window, self._on_key_input)
        # Set window as current context
        glfw.make_context_current(self._window)

        # Set options
        glEnable(GL_DEPTH_TEST)    #Enable Depth Buffer
	    # glDepthFunc(GL_LESS)
        glEnable(GL_BLEND)          #Colour

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self._background_color_night = v3([0.0, 0.05, 0.1])
        self._background_color_day = v3([0.6, 0.7, 0.75])

        # Camera
        self.sel_camera: str = "static"  # Selected camera mode
        self.update_camera: bool = True
        self._static_target: v3 = v3([0, 2.0, 0])  #Making camera look slightly up to the sky form the centre of the plane
        self._default_eye: v3 = v3([0, 8, 10]) #Default camera position, Camera is always looking along Z-axis ; called eye space

        # Matrices
        self._fov, self._near, self._far = None, None, None
        self._eye, self._target, self._up = None, None, None
        self.projection_matrix, self.view_matrix = None, None
        self._prepare_matrices()


        # Shaders
        self.shaders = {
            "phong": Shader("shaders/phong_vs.glsl", "shaders/phong_fs.glsl"),
            "light_source": Shader("shaders/light_source_vs.glsl", "shaders/light_source_fs.glsl"),
        }
        self.current_shader: Shader = None
        self._use_shader(self.shaders["phong"])

        #Sensitivity WASD
        self.xTrans, self.yTrans, self.zTrans = 0,0,0

        # Scene
        self.scene = {
            "Runway": LoadedObject("data/floor.obj", 0, 0, 0, 2.0),  #position and scaling
            "Center_Plane": LoadedObject("data/A380.obj", 0, 2.1, 0, scale=2),
            "Moving_Plane": LoadedObject("data/A380.obj"),
        }

        # Lighting
        self._point_light_obj = LoadedObject("data/uv_sphere.obj")  # sphere to represent point light sources

        self.sun_moon = DirLight(amb=v3([0.05, 0.05, 0.05]), dif=v3([0.4, 0.4, 0.8]), spe=v3([0.4, 0.4, 0.8]),
                                 direction=v3([-0.2, -1.0, -0.3]), uni_name="dirLight")
        point_lights = [
            #width, height, front
            (v3([10.0, 5.0, -8.0]), v3([1.0, 1.0, 1.0])),  # white
            (v3([0.0, 0.2, 0.0]), v3([0.3, 0.3, 1.0])),  #blue
            (v3([-10.0, 5.0, -8.0]), v3([1.0, 1.0, 0.3])),  #yellow
            (v3([0.0, 5.0, 0.0]), v3([1.0, 0.3, 0.3]))  # red
        ]
        self.point_lights = list(self._pl_gen(point_lights))

        self.spot_light_offset = v3([-1.0, 0.0, 0.0])  # Relative offset from moving plane
        self.spot_light_def_dir = v3([0.0, 0.0, 0.0])  # Default direction (same as moving plane)
        self.spot_light_angle_offset_x = 0  
        self.spot_light_angle_offset_y = 0
        self.spot_light = SpotLight(amb=v3([0.0, 0.0, 0.0]), dif=v3([0.0, 1.0, 0.5]), spe=v3([0.0, 1.0, 0.5]),
                                    k=v3([1.0, 0.07, 0.017]), pos=v3([0.0]*3), direction=self.spot_light_def_dir, #position is marked at headlight
                                    co=math.cos(math.radians(22.5)), oco=math.cos(math.radians(25.0)),
                                    uni_name="spotLight", lss=self.shaders["light_source"], obj=None)

    def _pl_gen(self, positions):
        """Point lights generator."""
        for i, (p, c) in enumerate(positions):
            light = PointLight(amb=0.05 * c, dif=1.0 * c, spe=1.0 * c,
                               k=v3([1.0, 0.07, 0.017]), pos=p,
                               uni_name=f"pointLights[{i}]", lss=self.shaders["light_source"],
                               obj=self._point_light_obj)
            yield light


    def _use_shader(self, shader: Shader) -> None:
        self.current_shader = shader
        self.current_shader.use()
        # Update matrices after changing shader
        self._update_projection()
        self._update_view()

    #Camera
    def _prepare_matrices(self) -> None:
        # Projection matrix
        self._fov = 45
        self._near = 0.1
        self._far = 100
        # View matrix
        self._eye: v3 = self._default_eye
        self._target: v3 = self._static_target
        self._up: v3 = v3([0, 1, 0])

    def _update_view(self) -> None:
        """Recalculate view matrix and upload it to shader."""
        self.view_matrix = lookAt.create_look_at(self._eye, self._target, self._up) 
        self.current_shader.set_view(self.view_matrix)  #Uploading to Shader 

    def _update_projection(self) -> None:
        """Recalculate projection matrix and upload it to shader."""
        a = self._width / self._height
        self.projection_matrix = Perspective_projection.create_perspective_projection(self._fov, a, self._near, self._far)
        self.current_shader.set_projection(self.projection_matrix) #Uploading to Shader

    def _on_resize(self, _window, width, height) -> None:
        self._width, self._height = width, height
        glViewport(0, 0, self._width, self._height)
        self._update_projection()

    def _on_key_input(self, _window, key, _scancode, action, _mode) -> None:
        left_right = {glfw.KEY_LEFT: 0.03, glfw.KEY_RIGHT: -0.03}
        if key in left_right and action != glfw.RELEASE:
            self.spot_light_angle_offset_x += left_right[key]
            return
        
        up_down = {glfw.KEY_DOWN: 0.03, glfw.KEY_UP: -0.03}
        if key in up_down and action != glfw.RELEASE:
            self.spot_light_angle_offset_y += up_down[key]
            if(self.spot_light_angle_offset_y <= 1.0 and self.spot_light_angle_offset_y >= -0.2):
                self.spot_light_angle_offset_y += up_down[key]
                print(self.spot_light_angle_offset_y)
            else:
                if self.spot_light_angle_offset_y > 1.0:
                    self.spot_light_angle_offset_y = 1.0
                elif self.spot_light_angle_offset_y < -0.2:
                    self.spot_light_angle_offset_y = -0.2
            return

        if key is glfw.KEY_S and action != glfw.RELEASE:
            self.xTrans -= 0.05
            return
        elif key is glfw.KEY_W and action != glfw.RELEASE:
            self.xTrans += 0.05
            return
        elif key is glfw.KEY_Q and action != glfw.RELEASE:
            self.yTrans -= 0.05
            return
        elif key is glfw.KEY_E and action != glfw.RELEASE:
            self.yTrans += 0.05
            return
        elif key is glfw.KEY_A and action != glfw.RELEASE:
            self.zTrans -= 0.05
            return
        elif key is glfw.KEY_D and action != glfw.RELEASE:
            self.zTrans += 0.05
            return
            
        if action != glfw.PRESS:
            return
        cam = {glfw.KEY_1: "static", glfw.KEY_2: "following", glfw.KEY_3: "moving"}
        if key in cam:
            self.sel_camera = cam[key]
            self.update_camera = True

    def _set_daytime(self):
        blend_factor = (math.sin(glfw.get_time() * 0.1) + 1) / 2
        c = self._background_color_day * (1 - blend_factor) + self._background_color_night * blend_factor

        #Changing Intensity of Day Light
        self.sun_moon._diffuse = 0.9 * c
        self.sun_moon._specular = 0.9 * c
        glClearColor(c[0], c[1], c[2], 1)  #RGBA

    def _move_objects(self) -> None:
        time = glfw.get_time()
        # Move and rotate Center_Plane
        rot_y = Arithmetic.create_from_y_rotation(-0.5 * time)
        translation = Arithmetic.create_from_translation(v3([0, math.sin(time) + 0.23, 0]))  #move up_down (in y dir)

        model = Arithmetic.multiply(translation, self.scene["Center_Plane"].pos)  # up-down movement
        self.scene["Center_Plane"].model = Arithmetic.multiply(rot_y, model)  # rotation
        
        # Move and orientate Moving_Plane
        translation = v3([-5 + self.xTrans, 0.2+ self.yTrans, self.zTrans])
        o = self.scene["Moving_Plane"]
        o.set_pos(translation)
        o.model = Arithmetic.multiply(Arithmetic.create_from_y_rotation(-self.spot_light_angle_offset_x - math.pi), o.model)
        o.model = Arithmetic.multiply(Arithmetic.create_from_z_rotation(-self.spot_light_angle_offset_y), o.model)

        # Move and orientate spotlight relatively to Moving_Plane
        pos = Arithmetic.multiply(Arithmetic.create_from_translation(self.spot_light_offset), o.model)
        self.spot_light.set_pos(Vector3.from_matrix44_translation(pos))
        light_dir = self._get_cockpit_look_dir() + self.spot_light_def_dir 
        self.spot_light.set_dir(light_dir)

    def _get_cockpit_look_dir(self):
        angle = math.pi / 2 + self.spot_light_angle_offset_x #translation by math.pi
        return v3([math.sin(angle), 0.0, math.cos(angle)])

    def _process_camera(self) -> None:
        if not self.update_camera:
            return

        if self.sel_camera == "static":
            self._eye = self._default_eye
            self._target = self._static_target
            self.update_camera = False  # Static camera needs to be calculated only once.
        elif self.sel_camera == "following":
            self._eye = self._default_eye
            self._target = Vector3.from_matrix44_translation(self.scene["Moving_Plane"].model)
        elif self.sel_camera == "moving":
            m = Arithmetic.multiply(Arithmetic.create_from_translation(v3([-0.9, 0.0, 0])), self.scene["Moving_Plane"].model)    #plane cockpit view
            self._eye = Vector3.from_matrix44_translation(m)
            self._target = self._eye + self._get_cockpit_look_dir()  # Front facing camera
        self._update_view()

    def _draw_light_sources(self) -> None:
        """Draws light sources with appropriate shaders."""
        self._use_shader(self.shaders["light_source"])
        for light in self.point_lights:
            light.draw()
        self.spot_light.draw()

    def _draw_objects(self) -> None:
        """Sets currently selected shader, then draws shaded objects."""
        self._use_shader(self.shaders["phong"])    #Select Phong Shader
        self.current_shader.set_v3("viewPos", self._eye)

        # Use lights
        self.sun_moon.use_light(self.current_shader)
        for light in self.point_lights:
            light.use_light(self.current_shader)
        self.spot_light.use_light(self.current_shader)

        # Draw objects
        for o in self.scene.values():
            o.draw(self.current_shader)

    def main_loop(self) -> None:
        while not glfw.window_should_close(self._window):
            glfw.poll_events()
	    # Clean the Back buffer and Depth buffer
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Update scene
            self._set_daytime()
            self._move_objects()
            self._process_camera()

            # Draw scene
            self._draw_light_sources()
            self._draw_objects()

            # Swap buffers
            glfw.swap_buffers(self._window)


def main():
    window = Window(1280, 720, "AirBus A380 Modeling")
    window.main_loop()
    glfw.terminate()


if __name__ == '__main__':
    main()



