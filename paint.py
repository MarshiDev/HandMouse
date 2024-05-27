import mediapipe as mp
import pygame
import time
import cv2


pygame.init()

mode = "pointer"
# mode = "wrist"

dims = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(dims, pygame.FULLSCREEN)
pygame.display.set_caption("HandPaint")
draw_surf = pygame.Surface(screen.get_size())
draw_surf.fill("white")

last_pos = [0, 0]
actual_pos = [dims[0] / 2, dims[1] / 2]
lerped_pos = [dims[0] / 2, dims[1] / 2]

mouse_down = False
smoothness = 0.6

running = True


def lerp(a, b, t):
    return (1 - t) * a + t * b


def callback_pointer(result: mp.tasks.vision.HandLandmarkerResult, *args):
    global actual_pos, last_pos, mouse_down
    if result.hand_landmarks:
        wrist = result.hand_landmarks[0][0]
        pointer = result.hand_landmarks[0][8]
        mouse_down = round(wrist.z - pointer.z, 3) * 1000 > 70

        new_pos = [(pointer.x - 0.5) * 2, (pointer.y - 0.5) * 2]
        delta = last_pos[0] - new_pos[0], last_pos[1] - new_pos[1]
        last_pos = new_pos
        actual_pos = [max(min(actual_pos[0] + round(delta[0], 4) * 1000, dims[0]), 0),
                      max(min(actual_pos[1] - round(delta[1], 4) * 1000, dims[0]), 0)]


def callback_normal(result: mp.tasks.vision.HandLandmarkerResult, *args):
    global actual_pos, last_pos, mouse_down
    if result.hand_landmarks:
        wrist = result.hand_landmarks[0][0]
        pointer = result.hand_landmarks[0][8]
        mouse_down = round(wrist.z - pointer.z, 3) * 1000 > 70

        new_pos = [(wrist.x - 0.5) * 2, (wrist.y - 0.5) * 2]
        delta = last_pos[0] - new_pos[0], last_pos[1] - new_pos[1]
        last_pos = new_pos
        actual_pos = [max(min(actual_pos[0] + round(delta[0], 4) * 1000, dims[0]), 0),
                      max(min(actual_pos[1] - round(delta[1], 4) * 1000, dims[0]), 0)]


options = mp.tasks.vision.HandLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path="./model/hand_landmarker.task"),
    running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
    result_callback=callback_pointer if mode == "pointer" else callback_normal
)


camera = cv2.VideoCapture(0)

with mp.tasks.vision.HandLandmarker.create_from_options(options) as landmarker:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cam_frame = camera.read()[1]

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cam_frame)
        landmarker.detect_async(mp_image, round(time.time() * 1000))

        lerped_pos[0] = lerp(lerped_pos[0], actual_pos[0], smoothness)
        lerped_pos[1] = lerp(lerped_pos[1], actual_pos[1], smoothness)

        if mouse_down:
            pygame.draw.circle(draw_surf, "black", lerped_pos, 5)

        screen.blit(draw_surf, (0, 0))
        pygame.draw.circle(screen, "red", lerped_pos, 3)

        cv2.waitKey(1)

        pygame.display.flip()

camera.release()
cv2.destroyAllWindows()
