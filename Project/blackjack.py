import copy
import random
import pygame
import os

# Constants

card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_suits = ['hearts', 'diamonds', 'clubs', 'spades']

# Create one deck with all suits
one_deck = []
for suit in card_suits:
    for value in card_values:
        one_deck.append((value, suit))

decks = 4
WIDTH = 700
HEIGHT = 750
fps = 60
CARD_SLIDE_DURATION = 20  # frames for card slide animation
results = ["","PLAYER BUSTED o_O", "PLAYER WINS :)", "DEALER WINS :(", "TIE GAME..."]


# Game setup

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
timer = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
pygame.mixer.init()

# Load card images
card_images = {}
for suit in card_suits:
    for value in card_values:
        # Build filename from card details
        if value == '10':
            filename = f'cards/10_of_{suit}.png'
        elif value == 'J':
            filename = f'cards/jack_of_{suit}.png'
        elif value == 'Q':
            filename = f'cards/queen_of_{suit}.png'
        elif value == 'K':
            filename = f'cards/king_of_{suit}.png'
        elif value == 'A':
            filename = f'cards/ace_of_{suit}.png'
        else:
            filename = f'cards/{value}_of_{suit}.png'
        
        if os.path.exists(filename):
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (120, 220))
            card_images[(value, suit)] = img

# Back of card image (placeholder)
card_back = pygame.Surface((120, 220))
card_back.fill('darkgreen')
pygame.draw.rect(card_back, 'white', card_back.get_rect(), 3)
back_font = pygame.font.Font('freesansbold.ttf', 20)
back_font.render('BACK', True, 'white')

# Modifiers

mod_lucky_start = "LUCKY START"
mod_dealer_19 = "DEALER 19"
mod_hidden_dealer = "HIDDEN DEALER"
mod_soft_aces = "NO SOFT ACES"


modifiers = [
    mod_lucky_start,
    mod_dealer_19,
    mod_hidden_dealer,
    mod_soft_aces,
    None
 
]

# game variables

active = False
records = [0, 0, 0]
player_score = 0
dealer_score = 0
start_new_hand = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False

# variables for implementing modifiers
current_modifier = None
dealer_stand_limit = 17
hidden_dealer_active = False
soft_aces_disabled = False

# Card animation tracking
card_animations = {}  # Store animation progress for each card

# intialising sounds
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
busted_sound = pygame.mixer.Sound("busted.wav")
tie_sound = pygame.mixer.Sound("tie.wav")
draw_sound = pygame.mixer.Sound("taking_playing_card.mp3")



# Helpfunction

def find_lucky_card(deck):
    for card in deck:
        if card[0] in ['10', 'J', 'Q', 'K']:
            return card
    return None

def start_new_round():
    global current_modifier, dealer_stand_limit, hidden_dealer_active, soft_aces_disabled

    current_modifier = random.choice(modifiers)

    dealer_stand_limit = 17
    hidden_dealer_active = False
    soft_aces_disabled = False

    if current_modifier == mod_dealer_19:
        dealer_stand_limit = 19
    
    if current_modifier == mod_hidden_dealer:
        hidden_dealer_active = True

    if current_modifier == mod_soft_aces:
        soft_aces_disabled = True

# functie voor intial deal zodat de modifiers kunnen toegepast worden
def initial_deal(my_hand, dealer_hand, deck):
    global card_animations
    # Lucky Start modifier
    if current_modifier == mod_lucky_start:
        lucky_card = find_lucky_card(deck)
        if lucky_card is not None:
            my_hand.append(lucky_card)
            deck.remove(lucky_card)
            # Start animation for lucky card
            card_animations[('player', len(my_hand) - 1)] = 0.0

        
    # vul kaarten aan tot 2 kaarten voor de speler
    while len(my_hand) < 2:
        my_hand, deck = deal_cards(my_hand, deck)

    # dealer krijgt 2 kaarten
    while len(dealer_hand) <  2:
        dealer_hand, deck = deal_cards(dealer_hand, deck)
    
    return my_hand, dealer_hand, deck

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck)-1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    
    # Play card deal sound
    draw_sound.play()
    
    # Start animation for the new card
    if current_hand == my_hand:
        card_key = ('player', len(current_hand) - 1)
    else:
        card_key = ('dealer', len(current_hand) - 1)
    card_animations[card_key] = 0.0
    
    return current_hand, current_deck

# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (415, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (415, 100))

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        x, y = 70 + (70 * i), 320 + (5 * i)
        card_key = ('player', i)
        
        # Check if card is animating
        if card_key in card_animations:
            progress = card_animations[card_key]
            # Slide from bottom (y + 100) to final position
            anim_y = y + 100 * (1 - progress)
            anim_x = x
        else:
            anim_x, anim_y = x, y
        
        # Draw card image if available
        if player[i] in card_images:
            screen.blit(card_images[player[i]], (anim_x, anim_y))
        else:
            # Fallback to colored rectangle
            pygame.draw.rect(screen, 'white', [anim_x, anim_y, 120, 220], 0, 5)
            screen.blit(font.render(player[i][0], True, 'black'), (anim_x + 5, anim_y + 5))
            pygame.draw.rect(screen, 'red', [anim_x, anim_y, 120, 220], 5, 5)
    
    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        x, y = 70 + (70 * i), 75 + (5 * i)
        card_key = ('dealer', i)
        
        # Check if card is animating
        if card_key in card_animations:
            progress = card_animations[card_key]
            # Slide from top (y - 100) to final position
            anim_y = y - 100 * (1 - progress)
            anim_x = x
        else:
            anim_x, anim_y = x, y
        
        if i != 0 or reveal:
            # Draw card image if available
            if dealer[i] in card_images:
                screen.blit(card_images[dealer[i]], (anim_x, anim_y))
            else:
                pygame.draw.rect(screen, 'white', [anim_x, anim_y, 120, 220], 0, 5)
                screen.blit(font.render(dealer[i][0], True, 'black'), (anim_x + 5, anim_y + 5))
                pygame.draw.rect(screen, 'blue', [anim_x, anim_y, 120, 220], 5, 5)
        else:
            # Hidden card
            screen.blit(card_back, (anim_x, anim_y))

# Update card animations
def update_animations():
    global card_animations
    keys_to_remove = []
    for key in card_animations:
        card_animations[key] += 1.0 / CARD_SLIDE_DURATION
        if card_animations[key] >= 1.0:
            card_animations[key] = 1.0
            keys_to_remove.append(key)
    
    # Remove finished animations
    for key in keys_to_remove:
        del card_animations[key]

# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = sum(1 for card in hand if card[0] == 'A')
    for i in range(len(hand)):
        card_value = hand[i][0]  # Extract value from (value, suit) tuple
        # 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if card_value == card_values[j]:
                hand_score += int(card_value)
        # for 10 and face cards, add 10
        if card_value in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif card_value == 'A':
            hand_score += 11
        # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if not soft_aces_disabled:
        if hand_score > 21 and aces_count > 0:
            for i in range(aces_count):
                if hand_score > 21:
                    hand_score -= 10
    return hand_score

# draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [200, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [200, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (215, 50))
        button_list.append(deal)
    # once game started, show hit and stand buttons and win/loss records
    else:
        hit = pygame.draw.rect(screen, 'white', [50, 600, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [50, 600, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (105, 635))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [350, 600, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [350, 600, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (405, 635))
        button_list.append(stand)
        
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (65, 710))
    ## if there is an outcome for the hand that was played, display a restart button and tell player what happened
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [200, 250, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [200, 250, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [203, 253, 294, 94], 3, 5)        
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (225, 280))
        button_list.append(deal)
    return button_list
    
    
    
# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add, dealer_limit):
    # check end game scenarios if player has stood, busted of blackjacked
    # result 1- player bust, 2- win, 3- loss, 4- push
    if not hand_act and deal_score >= dealer_limit:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1:
                busted_sound.play()
            elif result == 2:
                win_sound.play()
            elif result == 3:
                lose_sound.play()
            elif result == 4:
                tie_sound.play()

            
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add


# main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    update_animations()  # Update card animations every frame
    screen.fill('black')
    # initial deal to player and dealer
    if start_new_hand:
            my_hand, dealer_hand, game_deck = initial_deal(my_hand, dealer_hand, game_deck)
            start_new_hand = False
            active = True

    # once game is activated, and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if not hand_active:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < dealer_stand_limit:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)

    if active and current_modifier is not None:
        pygame.draw.rect(screen, (60, 60, 60), [0, 560, WIDTH, 40])
        info = smaller_font.render(f"Modifier: {current_modifier}", True, "yellow")
        screen.blit(info, (15, 565))

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    start_new_hand = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    reveal_dealer = False
                    outcome = 0
                    hand_active = True
                    add_score = True

                    # choose modifier for this round
                    start_new_round()
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    if not hidden_dealer_active:
                        reveal_dealer= True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        start_new_hand = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        reveal_dealer = False
                        outcome = 0
                        hand_active = True
                        add_score = True
                        player_score = 0
                        dealer_score = 0
                        start_new_round()

    # if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score, dealer_stand_limit)

    
    pygame.display.flip()
pygame.quit()