#version 330 core

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_color;
layout(location = 3) in vec3 a_normal;

out vec3 frag_pos;
out vec3 v_normal;
out vec3 v_color;
out vec2 v_texture;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    frag_pos = vec3(model * vec4(a_pos, 1.0));
    v_normal = mat3(transpose(inverse(model))) * a_normal;
    v_texture = a_texture;

    gl_Position = projection * view * model * vec4(a_pos, 1.0);
}