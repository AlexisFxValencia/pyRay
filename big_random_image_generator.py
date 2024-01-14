from OpenGL.GL import *
import pygame
import numpy as np

def generate_random_pixels(width, height):
    #return np.random.randint(0, 2, size=(height, width), dtype=np.uint8) * 255
    return np.random.rand(height, width).astype(np.float32) * 255

def generate_random_pixels_2(width, height):
    random_tiny = np.random.rand(height//10, width//10).astype(np.float32) * 255
    random_big = np.zeros((height, width))
    n_div = 10
    for j in range(height):
        for i in range(width):
            i_tiny = i/n_div - i%n_div
            random_big[i][j] = random_tiny[i_tiny]
    return random_big

def draw_image(image):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRasterPos2i(-1, -1)
    glDrawPixels(image.shape[1], image.shape[0], GL_LUMINANCE, GL_UNSIGNED_BYTE, image)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.OPENGL | pygame.DOUBLEBUF)
    
    #glOrtho(-1, 1, -1, 1, -1, 1)  # Set up orthographic projection

    image_width, image_height = 800, 600
    random_image = generate_random_pixels_2(image_width, image_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        draw_image(random_image)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
