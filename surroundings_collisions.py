EMPTY_CELL = 0
ICE_NUM = 1
FROZEN_FRUIT_NUM = 2
FRUIT_NUM = 3
IGLOO_NUM = 4
OFFSET = 5

SCREEN_DIMENSIONS = (800, 624)
FRAME_DIMENSIONS = (50, 48)

def get_valid_moves(player_rect, board, is_enemy=False):
    valid_moves = {"up" : True, "down" : True, "left" : True, "right" : True}

    check_for_frame_collisions(player_rect, valid_moves, is_enemy)
    check_for_igloo_collisions(player_rect, board, valid_moves)
    check_for_ice_collisions(player_rect, board, valid_moves)

    return valid_moves

def check_for_frame_collisions(player_rect, valid_moves, is_enemy):
    if player_rect.top < FRAME_DIMENSIONS[1]:
        player_rect.top = FRAME_DIMENSIONS[1]
        if is_enemy:
            valid_moves["up"] = False
    
    if player_rect.bottom > SCREEN_DIMENSIONS[1] - FRAME_DIMENSIONS[1]:
        player_rect.bottom = SCREEN_DIMENSIONS[1] - FRAME_DIMENSIONS[1]
        if is_enemy:
            valid_moves["down"] = False
    
    if player_rect.left < FRAME_DIMENSIONS[0]:
        player_rect.left = FRAME_DIMENSIONS[0]
        if is_enemy:
            valid_moves["left"] = False
    
    if player_rect.right > SCREEN_DIMENSIONS[0] - FRAME_DIMENSIONS[0]:
        player_rect.right = SCREEN_DIMENSIONS[0] - FRAME_DIMENSIONS[0] 
        if is_enemy:
            valid_moves["right"] = False 


def check_for_igloo_collisions(player_rect, board, valid_moves):
    if player_rect.bottom > 444:
        return
    if board[(player_rect.top + OFFSET - 48) // 44][(player_rect.left - 50) // 44] == IGLOO_NUM:
        valid_moves["left"] = False
    
    if board[(player_rect.bottom - OFFSET - 48) // 44][(player_rect.left - 50) // 44] == IGLOO_NUM:
        valid_moves["left"] = False

    if board[(player_rect.top + OFFSET - 48) // 44][(player_rect.right - 50) // 44] == IGLOO_NUM:
        valid_moves["right"] = False

    if board[(player_rect.bottom - OFFSET - 48) // 44][(player_rect.right - 50) // 44] == IGLOO_NUM:
        valid_moves["right"] = False

    if board[(player_rect.top - 48) // 44][(player_rect.left + OFFSET - 50) // 44] == IGLOO_NUM:
        valid_moves["up"] = False   

    if board[(player_rect.top - 48) // 44][(player_rect.right - OFFSET - 50) // 44] == IGLOO_NUM:
        valid_moves["up"] = False   

    if board[(player_rect.bottom - 48) // 44][(player_rect.left + OFFSET - 50) // 44] == IGLOO_NUM:
        valid_moves["down"] = False

    if board[(player_rect.bottom - 48) // 44][(player_rect.right - OFFSET - 50) // 44] == IGLOO_NUM:
        valid_moves["down"] = False

def check_for_ice_collisions(player_rect, board, valid_moves):
    if ICE_NUM <= board[(player_rect.top + OFFSET - 48) // 44][(player_rect.left - 50) // 44] <= FROZEN_FRUIT_NUM:
        valid_moves["left"] = False
    
    if ICE_NUM <= board[(player_rect.bottom - OFFSET - 48) // 44][(player_rect.left - 50) // 44] <= FROZEN_FRUIT_NUM:
        valid_moves["left"] = False

    if ICE_NUM <= board[(player_rect.top + OFFSET - 48) // 44][(player_rect.right - 50) // 44] <= FROZEN_FRUIT_NUM:
        valid_moves["right"] = False

    if ICE_NUM <= board[(player_rect.bottom - OFFSET - 48) // 44][(player_rect.right - 50) // 44] <= FROZEN_FRUIT_NUM:
        valid_moves["right"] = False

    if ICE_NUM <= board[(player_rect.top - 48) // 44][(player_rect.left + OFFSET - 50) // 44] <= FROZEN_FRUIT_NUM:
        valid_moves["up"] = False   

    if ICE_NUM <= board[(player_rect.top - 48) // 44][(player_rect.right - OFFSET - 50) // 44] <= FROZEN_FRUIT_NUM:
        valid_moves["up"] = False   

    if (player_rect.bottom - 48) // 44 >= len(board):
        return
    if ICE_NUM <= board[(player_rect.bottom - 48) // 44][(player_rect.left + OFFSET - 50) // 44] <= FROZEN_FRUIT_NUM:
        valid_moves["down"] = False

    if ICE_NUM <= board[(player_rect.bottom - 48) // 44][(player_rect.right - OFFSET - 50) // 44] <= FROZEN_FRUIT_NUM:
        valid_moves["down"] = False
