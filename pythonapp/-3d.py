    if keys[pygame.K_UP] and plant[pos] == entities['player']['pos'][0] + 1: print("plant found")
    if keys[pygame.K_DOWN]: print(entities['player']['pos'][0] - 1)
    if keys[pygame.K_LEFT]: print(entities['player']['pos'][1] + 1)
    if keys[pygame.K_RIGHT]: print(entities['player']['pos'][1] - 1)