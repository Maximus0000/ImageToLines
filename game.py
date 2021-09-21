import pygame
import main

pygame.init()
window = pygame.display.set_mode((600, 600))
val1 ,val2, val3 = 200,150,60
factor = 2
amount = 100
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                val1 += 10
            if event.key == pygame.K_s:
                val1 -= 10
            if event.key == pygame.K_e:
                val2 += 10
            if event.key == pygame.K_d:
                val2 -= 10
            if event.key == pygame.K_r:
                val3 += 10
            if event.key == pygame.K_f:
                val3 -= 10
            if event.key == pygame.K_t:
                factor += 1
            if event.key == pygame.K_g:
                factor -= 1
            if event.key == pygame.K_z:
                amount += 100
            if event.key == pygame.K_h:
                amount -= 100
                amount = max([amount,50])
    window.fill(0)

    rect = pygame.Rect(window.get_rect().center, (0, 0)).inflate(*([min(window.get_size())//2]*2))

    pixel_array = pygame.PixelArray(window)
    try:
        arr = main.linify(criticalValues=(val1 ,val2, val3),factor = factor, amountDataspoints=amount)
        size = arr.shape
        print(size)
    
        for i in range(size[0]):
            for j in range(size[1]):
                pixel_array[j,i] = (arr[i,j],arr[i,j],arr[i,j])
    except:
        pass
    pixel_array.close()
    
    pygame.display.flip()

pygame.quit()
exit()
