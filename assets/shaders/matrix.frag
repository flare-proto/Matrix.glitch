#version 330
in vec2 texCoords;
out vec4 fragColor;

uniform sampler2D screenTexture;
uniform float time;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main()
{
    vec2 uv = texCoords;

    // Simulate "columns" of rain
    float column = floor(uv.x * 80.0);

    // Random fall speed per column
    float speed = random(vec2(column, 0.0)) * 2.0 + 1.0;

    // Offset by time
    float y = fract(uv.y + time * 0.2 * speed);

    // Create glowing band
    float glow = smoothstep(0.02, 0.0, abs(y - 0.5));

    // Color: greenish
    vec3 color = vec3(0.0, 1.0, 0.3) * glow;

    // Blend with original screen
    vec3 sceneColor = texture(screenTexture, uv).rgb;
    fragColor = vec4(sceneColor + color, 1.0);
}
