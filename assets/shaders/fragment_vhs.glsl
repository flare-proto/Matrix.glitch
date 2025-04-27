#version 330
in vec2 fragmentTexCoord;
out vec4 fragColor;

uniform sampler2D imageTexture;

uniform float time;

float rand(vec2 co) {
    return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    vec2 uv = fragmentTexCoord;
    
    // SMALL random horizontal band offset            0.02          V
    float glitch = (rand(vec2(time * 0.2, uv.y * 30.0)) - 0.5) * 0.005;
    uv.x += glitch;

    // SMALLER RGB Split 0.003
    float splitAmount = 0.0015;
    float r = texture(imageTexture, uv + vec2(splitAmount, 0.0)).r;
    float g = texture(imageTexture, uv).g;
    float b = texture(imageTexture, uv - vec2(splitAmount, 0.0)).b;

    fragColor = vec4(r, g, b, 1.0);
}