from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram, ShaderProgram
import Vector3 as v3


class Shader:
    def __init__(self, vs: str, fs: str):
        """Shader program wrapper. Compiled and prepared for use.

        :param vs: Vertex shader filepath.
        :param fs: Fragment shader filepath.
        """
        self._vs_path = vs
        self._fs_path = fs
        self._shader = self._compile_shader()

        # Assumption: all shaders will have these uniforms.
        self._loc = {
            "model": glGetUniformLocation(self._shader, "model"),
            "projection": glGetUniformLocation(self._shader, "projection"),
            "view": glGetUniformLocation(self._shader, "view"),
        }

    def use(self) -> None:
        glUseProgram(self._shader)

    def set_model(self, matrix) -> None:
        glUniformMatrix4fv(self._get_loc("model"), 1, GL_FALSE, matrix)

    def set_projection(self, matrix) -> None:
        glUniformMatrix4fv(self._get_loc("projection"), 1, GL_FALSE, matrix)

    def set_view(self, matrix) -> None:
        glUniformMatrix4fv(self._get_loc("view"), 1, GL_FALSE, matrix)

    def set_bool(self, uniform_name: str, val: bool) -> None:
        glUniform1i(self._get_loc(uniform_name), val)

    def set_float(self, uniform_name: str, val: float) -> None:
        glUniform1f(self._get_loc(uniform_name), val)

    def set_v3(self, uniform_name: str, val: v3) -> None:
        glUniform3fv(self._get_loc(uniform_name), 1, val)

    def _get_loc(self, uniform_name: str) -> None:
        """Lazy uniform location storage."""
        if uniform_name not in self._loc:
            self._loc[uniform_name] = glGetUniformLocation(self._shader, uniform_name)
        return self._loc[uniform_name]

    def _compile_shader(self) -> ShaderProgram:
        """
        Compile shaders from given source files.

        :return: Compiled shader program.
        """
        vert_shader = self._load_shader(self._vs_path)
        frag_shader = self._load_shader(self._fs_path)

        shader = compileProgram(compileShader(vert_shader, GL_VERTEX_SHADER),
                                compileShader(frag_shader, GL_FRAGMENT_SHADER))
        return shader

    @staticmethod
    def _load_shader(shader_file: str) -> bytes:
        with open(shader_file) as f:
            shader_source = f.read()
        return str.encode(shader_source)
