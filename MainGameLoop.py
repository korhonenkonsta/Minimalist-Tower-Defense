import pygame

from math import sqrt
from operator import pos

from Map import *
from EnemyUnits import *
from Towers import *
from Player import *

# Vareja
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)


#-----------------------------MAIN PROGRAM----------------------------- 
# Alustaa Pygamen
pygame.init()
 
# Asettaa screenin mitat
screen_width = 1024
screen_height = 576
screen = pygame.display.set_mode([screen_width, screen_height])
# Kentan leveys
map_width = 750
# Screenin ulkopuolisen marginaalin leveys, kaytetaan vihollisten poistamisessa
screen_marginal = 30

#-----------------------------UI-------------------------------------

# Fontti
font = pygame.font.Font(None, 24)
font_2 = pygame.font.Font(None, 22)

# Lataillaan kuvia
basic_tower_button = pygame.image.load("basic_tower_button.png")
basic_tower_button_select_green = pygame.image.load("select_green.png")

piercing_tower_button = pygame.image.load("piercing_tower_button.png")
piercing_tower_button_select_green = pygame.image.load("select_green.png")

upgrade_button = pygame.image.load("upgrade_button.png")
upgrade_button_select_green = pygame.image.load("select_green.png")

sell_button = pygame.image.load("sell_button.png")
sell_button_select_green = pygame.image.load("select_green.png")

next_wave_button = pygame.image.load("next_wave_button.png")
next_wave_button_select_green = pygame.image.load("next_wave_button_select_green.png")

main_menu_button = pygame.image.load("main_menu_button.png")
main_menu_button_select_green = pygame.image.load("menu_button_select_green.png")

quit_game_button = pygame.image.load("quit_game_button.png")
quit_game_button_select_green = pygame.image.load("menu_button_select_green.png")

play_button = pygame.image.load("play_button.png")
play_button_select_green = pygame.image.load("menu_button_select_green.png")

main_menu_screen = pygame.image.load("main_menu_screen.png")
game_over_screen = pygame.image.load("game_over_screen.png")

# Luo suorakulmaisen objektin jolla on ladatun kuvan mitat. Sen paikkaa voi siirtaa 
# maarittamalla koordinaatit rect.x ja rect.y ja pygame piirtaa kuvan tahan sijaintiin.
basic_tower_select_rect = basic_tower_button.get_rect()
basic_tower_select_rect.x = 764
basic_tower_select_rect.y = 192

piercing_tower_select_rect = piercing_tower_button.get_rect()
piercing_tower_select_rect.x = 764+62
piercing_tower_select_rect.y = 192

next_wave_select_rect = next_wave_button.get_rect()
next_wave_select_rect.x = 762
next_wave_select_rect.y = 120

upgrade_select_rect = upgrade_button.get_rect()
upgrade_select_rect.x = 764
upgrade_select_rect.y = 50

sell_select_rect = sell_button.get_rect()
sell_select_rect.x = 764 + 70
sell_select_rect.y = 50

play_select_rect = play_button.get_rect()
play_select_rect.x = 392
play_select_rect.y = 298

main_menu_select_rect = main_menu_button.get_rect()
main_menu_select_rect.x = 392
main_menu_select_rect.y = 298

quit_select_rect = quit_game_button.get_rect()
quit_select_rect.x = 392
quit_select_rect.y = 366

#----------------------------Tarvittavat oliot--------------------------------------

# Luodaan taso
map = Map()
# Piirretaan vihollisten reitti
map.draw_path()
# Luodaan pelaaja
player = Player()
# Luodaan aallot
wave = EnemyWave()
# Ruudunpaivitysta varten
clock = pygame.time.Clock()

# --------------------------------Groupit---------------------------------------------

# Listat spriteista, joita hallitsee luokka Group tai tarkempaa tietoa tarvittaessa LayeredUpdates
enemy_list = pygame.sprite.LayeredUpdates()
bullet_list = pygame.sprite.Group()
tower_list = pygame.sprite.Group()
effect_list = pygame.sprite.Group()
towerpositioner_list = pygame.sprite.GroupSingle()
all_sprites_list = pygame.sprite.Group()

#---------------------------------Muuttujia----------------------------------------

# Vihollisaaltoja koskevat muuttujat
wave_enemies = 1
enemy_class_count = 1
wave_part_index = 0
last_path_point_index = len(map.path)
wave_is_done = True

# Peli on kaynnissa
game_is_on = True
# Main menu screen nakyy aluksi
show_main_menu = True
# Rakentamiseen
can_build = True
ready_to_build = False
# Muut screenit eivat nay
show_game = False
show_game_over = False


# ---------------------------- Main Game Loop ---------------------------------------

# Toistetaan kunnes kayttaja lopettaa pelin
while game_is_on:
    # Kun ollaan paavalikossa
    while show_main_menu:
        # Pygamen tapahtumajono
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                game_is_on = False
                show_main_menu = False
            #Jos hiiren painiketta klikataan
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Jos hiiren vasenta painiketta klikataan
                if event.button == 1:
                    # Hiiren koordinaatit klikkauskohdassa
                    click_position = pygame.mouse.get_pos()
                    # Jos painetaan play-nappulaa
                    if play_select_rect.collidepoint(click_position):
                        show_game = True
                        show_main_menu = False
                        
                        # Resetoidaan arvot uutta pelia varten
                        first_wave = True
                        wave_is_done = True
                        enemy_class_count = 1
                        # Aloitusrahat ja hp
                        player.gold = player.starting_gold
                        player.hp = player.starting_hp
                        #
                        chosen_tower = None
                        wave.wave_number = wave.starting_wave_number
                        wave.visible_wave_number = wave.starting_visible_wave_number
                        # Tyhjennetaan sprite-listat
                        bullet_list.empty()
                        enemy_list.empty()
                        tower_list.empty()
                        all_sprites_list.empty()
                        
                    # Jos painetaan quit-nappulaa
                    if quit_select_rect.collidepoint(click_position):
                        game_is_on = False
                        show_main_menu = False
        
        # Osoittimen sijainti
        mouse_position = pygame.mouse.get_pos()
        
        mouse_position_on_play_button = False
        mouse_position_on_quit_button = False
        
        # Blit piirtaa surfacen toiselle surfacelle, esim kuvan kuvalle tai screenille
        screen.blit(main_menu_screen,(0,0))
        screen.blit(play_button,(392,298))
        screen.blit(quit_game_button,(392,366))
        
        # Vihrea reunus kun hiiri on nappulan paalla
        if play_select_rect.collidepoint(mouse_position):
            mouse_position_on_play_button = True
            screen.blit(play_button_select_green,(394,300))
            
        if quit_select_rect.collidepoint(mouse_position):
            mouse_position_on_quit_button = True
            screen.blit(quit_game_button_select_green,(394,368))
       
        # Paivitetaan screen
        pygame.display.flip()
    
        # 60fps
        clock.tick(60)
        
        
    # Kun ollaan game over -ruudussa
    while show_game_over:
        # Pygamen tapahtumajono
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                game_is_on = False
                show_game_over = False
            #Jos hiiren painiketta klikataan
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Jos hiiren vasenta painiketta klikataan
                if event.button == 1:
                    # Hiiren koordinaatit klikkauskohdassa
                    click_position = pygame.mouse.get_pos()
                    if main_menu_select_rect.collidepoint(click_position):
                        show_game_over = False
                        show_main_menu = True
                    if quit_select_rect.collidepoint(click_position):
                        game_is_on = False
                        show_game_over = False
        # Osoittimen sijainti
        mouse_position = pygame.mouse.get_pos()
        
        mouse_position_on_main_menu_button = False
        mouse_position_on_quit_button = False
        
        screen.blit(game_over_screen,(0,0))
        screen.blit(main_menu_button,(392,298))
        screen.blit(quit_game_button,(392,366))
    
        if play_select_rect.collidepoint(mouse_position):
            mouse_position_on_main_menu_button = True
            screen.blit(main_menu_button_select_green,(394,300))
            
        if quit_select_rect.collidepoint(mouse_position):
            mouse_position_on_quit_button = True
            screen.blit(quit_game_button_select_green,(394,368))
       
        # Paivitetaan screen
        pygame.display.flip()
    
        # 60fps
        clock.tick(60)
        
    # Kun ollaan varsinaisessa pelissa
    while show_game: 
        # Pygamen tapahtumajono
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                game_is_on = False
                show_game = False
            
            #Jos hiiren painiketta klikataan
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Jos hiiren vasenta painiketta klikataan
                if event.button == 1:
                    # Hiiren koordinaatit klikkauskohdassa
                    click_position = pygame.mouse.get_pos()
                    # Jos ollaan valittu rakennettava torni
                    if ready_to_build and player.gold >= build.price:
                        # Ei voi rakentaa hudin paalle
                        if click_position[0] < map_width - screen_marginal/2:
                            # Ei voi rakentaa vihollisten reitin paalle tai muiden tornien paalle
                            for click in map.path_hitbox_list:
                                if click.collidepoint(mouse_position):
                                    can_build = False
                            for click in tower_list:
                                if click.rect.collidepoint(mouse_position):
                                    can_build = False
                                
                            if can_build == True:
                                # Luodaan torni         
                                tower = Tower(click_position, tower_class)
                                tower_list.add(tower)
                                all_sprites_list.add(tower)
                                # Peritaan maksu
                                player.gold -= tower.price
                                
                        
                    # Jos hiiri on torninappulan paalla
                    elif basic_tower_select_rect.collidepoint(click_position):
                        # Tornin tyyppi
                        tower_class = "basic tower"
                        # Luodaan hiiren koordinaatteja seuraava Builder-olion objekti valitusta tornista
                        build = Builder(click_position, tower_class)
                        towerpositioner_list.add(build)
                        all_sprites_list.add(build)
                        ready_to_build = True
                        
                    elif piercing_tower_select_rect.collidepoint(click_position):
                        # Tornin tyyppi
                        tower_class = "piercing tower"
                        # Luodaan hiiren koordinaatteja seuraava Builder-olion objekti valitusta tornista
                        build = Builder(click_position, tower_class)
                        towerpositioner_list.add(build)
                        all_sprites_list.add(build)
                        ready_to_build = True
                        
                    # Jos hiiri on next_wave-nappulan paalla
                    elif next_wave_select_rect.collidepoint(click_position) and wave_is_done:
                        if first_wave:
                            current_wave = wave.get_wave(wave.wave_number)
                            wave_part_index = 0
                            wave.wave_number += 1
                            first_wave = False
                            wave_is_done = False
                        
                        elif wave.visible_wave_number < wave.wave_count:
                            current_wave = wave.get_wave(wave.wave_number)
                            wave_part_index = 0
                            wave.wave_number += 1
                            wave.visible_wave_number += 1
                            wave_is_done = False
                   
                        
                    
                    # Tornin valinta
                    for tower in tower_list:
                        if tower.rect.collidepoint(click_position) and ready_to_build == False:
                            chosen_tower = tower
                            
                    # Jos torni on valittu
                    if chosen_tower:
                        # Tornin kehitys
                        if upgrade_select_rect.collidepoint(click_position):
                            if player.gold >= chosen_tower.upgrade_price:
                                if chosen_tower.level < 5:
                                    chosen_tower.upgrade(player)
                                    
                        # Tornin myynti
                        if sell_select_rect.collidepoint(click_position):
                            chosen_tower.sell_tower(player)
                            chosen_tower = None
                        
                #Jos hiiren oikeata painiketta klikataan
                elif event.button == 3: 
                    if ready_to_build:
                        ready_to_build = False 
                        towerpositioner_list.sprite.kill() 
                    chosen_tower = None
        
        # Osoittimen sijainti
        mouse_position = pygame.mouse.get_pos()
        
        
    #------------------Tornien toiminta--------------------------------------
    
        for tower_unit in tower_list:
            # Lataus
            tower_unit.reload -= 1
            
            if len(enemy_list) > 0:
                # Haetaan kohde
                tower_unit.target = tower_unit.get_target(enemy_list,tower_unit)
                if tower_unit.reload <= 0 and tower_unit.distance_to_enemy <= tower_unit.range:
                    if tower_unit.target in enemy_list:
                        # Ampuminen
                        tower_unit.fire(tower_unit.target)
                        bullet_list.add(tower_unit.bullet)
                        all_sprites_list.add(tower_unit.bullet)
                
                    
        can_build = True
        
    #------------------Vihollisten luonti aalloissa--------------------------------------
        
        if wave_is_done == False:
                
            if wave.visible_wave_number <= wave.wave_count:
                #Luo vihollisia aallon verran tasaisin valein 
                if wave_part_index <= len(current_wave)-1:
                    if enemy_class_count <= current_wave[wave_part_index][1]:
                        if wave.spawn_interval == 0:
                            # Luo vihollisen
                            enemy = EnemyUnit(map.path[0],current_wave[wave_part_index][0], map, 0, 1)
                             
                            # Lisaa vihollisen objektilistoihin
                            enemy_list.add(enemy)
                            all_sprites_list.add(enemy)
                            enemy_class_count += 1
                            wave.spawn_interval = 30
                    else:
                        wave_part_index += 1
                        enemy_class_count = 1
                else:
                    wave_part_index = 0
                    wave_is_done = True
                    
        elif wave.visible_wave_number == wave.wave_count and len(enemy_list) == 0:
            show_game = False
            show_game_over = True
                        
                        
    #------------------------Vihollisten liikkuminen----------------------------------
    
        if len(enemy_list) > 0:

            for enemy_unit in enemy_list:
                # Liikutetaan vihollista
                enemy_unit.move_enemy_unit()
                # Vihollisten poistaminen reitin lopussa
                if enemy_unit.next_path_part_index >= last_path_point_index-1 and enemy_unit.direction == "left" and enemy_unit.rect.centerx < map.path[last_path_point_index-1][0]:
                    enemy_list.remove(enemy_unit)
                    all_sprites_list.remove(enemy_unit)
                    player.hp -= 1
                
                if enemy_unit.next_path_part_index >= last_path_point_index-1 and enemy_unit.direction == "up" and enemy_unit.rect.centery < map.path[last_path_point_index-1][1]:
                    enemy_list.remove(enemy_unit)
                    all_sprites_list.remove(enemy_unit)
                    player.hp -= 1
                
                if enemy_unit.next_path_part_index >= last_path_point_index-1 and enemy_unit.direction == "down" and enemy_unit.rect.centery > map.path[last_path_point_index-1][1]:
                    enemy_list.remove(enemy_unit)
                    all_sprites_list.remove(enemy_unit)
                    player.hp -= 1
        # Jos elamat alle 0, naytetaan game over -screen
        if player.hp <= 0:
            show_game_over = True
            show_game = False
                
    #------------------------Ammuksien toiminta--------------------------------------
    
        for bullet_unit in bullet_list:
            # Suunta
            dir = bullet_unit.get_bullet_direction(bullet_unit.target, enemy_list)
            if dir == True:
                bullet_list.remove(bullet_unit)
                all_sprites_list.remove(bullet_unit)
            else:
                # Liikutetaan haettuun suuntaan
                 bullet_unit.move_bullet(dir)
            
           
            # Tarkistetaan osuuko
            enemy_hit_list = pygame.sprite.spritecollide(bullet_unit, enemy_list, False)
            
            # Jos osuu, poistetaan ammus ja vihollinen
            for enemy in enemy_hit_list:
                explosion = Effect(enemy.rect.center)
                effect_list.add(explosion)
                all_sprites_list.add(explosion)
                if not bullet_unit.bullet_type == "piercing":
                    # Poistaa ammuksen kaikista listoista
                    bullet_unit.kill()
                    
                # Poistaa vihollisen kaikista listoista
                enemy.kill()
                player.gold += 1
                # Kun iso vihollinen tuhoutuu, luodaan pienempi tilalle
                if enemy.enemy_class == "ball_3":
                    new_enemy = EnemyUnit(enemy.rect.center, "ball_2", map, enemy.current_path_part_index, enemy.current_path_part_index + 1)
                    enemy_list.add(new_enemy)
                    all_sprites_list.add(new_enemy)
                if enemy.enemy_class == "ball_2":
                    new_enemy = EnemyUnit(enemy.rect.center, "ball_1", map, enemy.current_path_part_index, enemy.current_path_part_index + 1)
                    enemy_list.add(new_enemy)
                    all_sprites_list.add(new_enemy)
            
            # Poistetaan kentan ulkopuolelle joutuvat ammukset
            if bullet_unit.rect.centerx < -screen_marginal or bullet_unit.rect.centery < -screen_marginal or bullet_unit.rect.centerx > (map_width) or bullet_unit.rect.centery > (screen_height + screen_marginal):
                bullet_list.remove(bullet_unit)
                all_sprites_list.remove(bullet_unit)
            
            # Jos ammus jaa ruudulle pidemmaksi aikaa
            if bullet_unit.lifetime > 240:
                bullet_list.remove(bullet_unit)
                all_sprites_list.remove(bullet_unit)
        
        # Efektien poisto
        for effect in effect_list:
            effect.effect_duration -= 1
            if effect.effect_duration == 0:
                effect.kill()
                        
        # Aikaa vihollisen luomiseen vahennetaan 
        if wave.spawn_interval > 0:
            wave.spawn_interval -= 1
        
        
    #----------------------Paivitys----------------------------------
    
        # Kutsutaan update-metodia spriteille
        all_sprites_list.update()
        
        # Screenin tyhjennys
        screen.fill(WHITE)
        
        
    #--------------------------HUD-tekstit------------------------------------
        
        # Rahat
        gold_text = font.render("GOLD:"+str(player.gold), 1, (0, 0, 0))
        gold_textpos = gold_text.get_rect()
        
        gold_textpos.x = 762
        gold_textpos.y = 10
        
        screen.blit(gold_text, gold_textpos)
        
        # Elamat
        hp_text = font.render("HP:"+str(player.hp), 1, (0, 0, 0))
        hp_textpos = hp_text.get_rect()
        
        hp_textpos.x = 762
        hp_textpos.y = 30
        
        screen.blit(hp_text, hp_textpos)
        
        # Aallot
        wave_nbr_text = font.render("WAVE:"+str(wave.visible_wave_number)+"/"+str(wave.wave_count), 1, (0, 0, 0))
        wave_nbr_textpos = wave_nbr_text.get_rect()
        
        wave_nbr_textpos.x = 832
        wave_nbr_textpos.y = 30
        
        screen.blit(wave_nbr_text, wave_nbr_textpos)
        
        # Info valitusta tornista
        if chosen_tower:
            
            tower_level_text = font.render("LEVEL:"+str(chosen_tower.level), 1, (0, 0, 0))
            tower_range_text = font.render("RANGE:"+str(chosen_tower.range), 1, (0, 0, 0))
            tower_price_text = font.render("PRICE:"+str(chosen_tower.price), 1, (0, 0, 0))
            tower_upgrade_price_text = font.render("UPGRADE PRICE:"+str(chosen_tower.upgrade_price), 1, (0, 0, 0))
            tower_reload_time_text = font_2.render("RELOAD T:"+str(chosen_tower.reload_time), 1, (0, 0, 0))
            tower_info_text = font.render("INFO:"+str(chosen_tower.tower_info), 1, (0, 0, 0))
            
        if ready_to_build:
            
            chosen_tower = None
            towerpositioner_list.sprite.move(mouse_position)
            
            tower_level_text = font.render("LEVEL:"+str(build.level), 1, (0, 0, 0))
            tower_range_text = font.render("RANGE:"+str(build.range), 1, (0, 0, 0))
            tower_price_text = font.render("PRICE:"+str(build.price), 1, (0, 0, 0))
            tower_upgrade_price_text = font.render("UPGRADE PRICE:"+str(build.upgrade_price), 1, (0, 0, 0))
            tower_reload_time_text = font_2.render("RELOAD T:"+str(build.reload_time), 1, (0, 0, 0))
            tower_info_text = font.render("INFO:"+str(build.tower_info), 1, (0, 0, 0))
            
            cancel_text = font.render("RIGHT CLICK TO CANCEL", 1, (0, 0, 0))
            cancel_textpos = cancel_text.get_rect()
            cancel_textpos.x = 763
            cancel_textpos.y = 550
            screen.blit(cancel_text, cancel_textpos)
            
        if not ready_to_build and not chosen_tower:
            
            tower_level_text = font.render("LEVEL:", 1, (0, 0, 0))
            tower_range_text = font.render("RANGE:", 1, (0, 0, 0))
            tower_price_text = font.render("PRICE:", 1, (0, 0, 0))
            tower_upgrade_price_text = font.render("UPGRADE PRICE:", 1, (0, 0, 0))
            tower_reload_time_text = font_2.render("RELOAD T:", 1, (0, 0, 0))
            tower_info_text = font.render("INFO:", 1, (0, 0, 0))
            
        tower_level_textpos = tower_level_text.get_rect()
        tower_range_textpos = tower_range_text.get_rect()
        tower_price_textpos = tower_price_text.get_rect()
        tower_upgrade_price_textpos = tower_upgrade_price_text.get_rect()
        tower_reload_time_textpos = tower_reload_time_text.get_rect()
        tower_info_textpos = tower_info_text.get_rect()
        
        # Tekstien sijainnit
        tower_level_textpos.x = 900
        tower_level_textpos.y = 50
        
        tower_range_textpos.x = 900
        tower_range_textpos.y = 70
        
        tower_price_textpos.x = 763
        tower_price_textpos.y = 480
        
        tower_upgrade_price_textpos.x = 763
        tower_upgrade_price_textpos.y = 500
        
        tower_reload_time_textpos.x = 900
        tower_reload_time_textpos.y = 90
        
        tower_info_textpos.x = 763
        tower_info_textpos.y = 450
        
        # Piirretaan tekstit
        screen.blit(tower_level_text, tower_level_textpos)
        screen.blit(tower_range_text, tower_range_textpos)
        screen.blit(tower_price_text, tower_price_textpos)
        screen.blit(tower_upgrade_price_text, tower_upgrade_price_textpos)
        screen.blit(tower_reload_time_text, tower_reload_time_textpos)
        screen.blit(tower_info_text, tower_info_textpos)
        
        
    #-------------------------------UI---------------------------------
    
        # Piirretaan kayttoliittyman elementit
        screen.blit(map.hud,(0,0))
        screen.blit(basic_tower_button,(764,192))
        screen.blit(piercing_tower_button,(826,192))
        screen.blit(next_wave_button,(762,120))
        screen.blit(upgrade_button,(762,50))
        screen.blit(sell_button,(832,50))
        
        
        # Vihreat reunukset
        if basic_tower_select_rect.collidepoint(mouse_position):
            screen.blit(basic_tower_button_select_green,(764,192))
        
        if piercing_tower_select_rect.collidepoint(mouse_position):
            screen.blit(piercing_tower_button_select_green,(826,192))
            
        if next_wave_select_rect.collidepoint(mouse_position):
            screen.blit(next_wave_button_select_green,(764,122))
        
        if upgrade_select_rect.collidepoint(mouse_position):
            screen.blit(upgrade_button_select_green,(764,52))
            
        if sell_select_rect.collidepoint(mouse_position):
            screen.blit(sell_button_select_green,(834,52))
        
        # Piirretaan tornin rangea kuvaava ympyra muiden pintojen paalle
        if ready_to_build:
            pygame.draw.circle(screen, RED, mouse_position, build.range, 1)
        if chosen_tower:
            pygame.draw.circle(screen, RED, chosen_tower.rect.center, chosen_tower.range, 1)
        
    #------------------------------------------------------------
    
        # Piirretaan spritet
        all_sprites_list.draw(screen)
     
        # Paivitetaan screen
        pygame.display.flip()
     
        # 60fps
        clock.tick(60)
 
pygame.quit()