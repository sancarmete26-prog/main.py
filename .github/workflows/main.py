import pygame
import sys
import random

# --- 1. HIZLI BAŞLATMA ---
pygame.init()
# Performans için çözünürlüğü bir tık optimize ettik
sw, sh = 480, 800 
screen = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

def resim_hazirla(isim, bx, by, renk):
    try:
        # .convert() komutu resmi ekran kartının formatına çevirir, kasmayı %80 azaltır!
        img = pygame.image.load(isim).convert_alpha()
        return pygame.transform.scale(img, (bx, by))
    except:
        s = pygame.Surface((bx, by))
        s.fill(renk)
        return s

# Görselleri yükle ve belleğe sabitle
dusman_img = resim_hazirla('BERKE.jpg', 80, 120, (200, 50, 50))
silah_img = resim_hazirla('silah.png', 180, 130, (50, 50, 50))

# --- 2. DEĞİŞKENLER ---
skor = 0
oyuncu_x = sw // 2
mermiler = []
# Düşman sayısını kasmaması için 3'e sabitledik ama hızlarını artırdık
dusmanlar = [[random.randint(50, sw-80), random.randint(-600, -100), random.randint(6, 10)] for _ in range(3)]

# --- 3. ANA DÖNGÜ ---
running = True
while running:
    # Arka planı düz siyah yapmak işlemciyi en az yoran yöntemdir
    screen.fill((10, 10, 15)) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mermi ekle
            mermiler.append([oyuncu_x + 35, sh - 150])

    # Parmak takibi
    mx, my = pygame.mouse.get_pos()
    oyuncu_x = mx - 40 

    # Mermi Hareketleri (Daha hızlı döngü)
    for m in mermiler[:]:
        m[1] -= 20 
        pygame.draw.rect(screen, (255, 255, 0), (m[0], m[1], 6, 15)) 
        if m[1] < 0: mermiler.remove(m)

    # Düşman Hareketleri ve Vurulma
    for d in dusmanlar:
        d[1] += d[2]
        screen.blit(dusman_img, (d[0], d[1]))
        
        # Çarpışma Testi (Daha basit matematik = daha az kasma)
        for m in mermiler[:]:
            if d[1] + 120 > m[1] > d[1] and d[0] < m[0] < d[0] + 80:
                skor += 1
                d[1] = random.randint(-400, -100)
                d[0] = random.randint(50, sw-80)
                mermiler.remove(m)
        
        if d[1] > sh:
            d[1] = random.randint(-400, -100)
            d[0] = random.randint(50, sw-80)

    # Silahı Çiz
    screen.blit(silah_img, (oyuncu_x, sh - 150))
    
    # Skor Yazısı (Hafif font kullanımı)
    try:
        font = pygame.font.SysFont("monospace", 35, bold=True)
        screen.blit(font.render(f"LES: {skor}", True, (255, 255, 0)), (20, 30))
    except: pass

    pygame.display.flip()
    # 60 FPS telefonunu zorluyorsa burayı 30 yapabilirsin
    clock.tick(45) 

pygame.quit()
      
