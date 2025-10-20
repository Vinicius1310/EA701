# BitDogLab v7
from machine import Pin, I2C
import time

# ===================== LEDs RGB =======================
led_red = Pin(11, Pin.OUT)
led_green = Pin(12, Pin.OUT)  
led_blue = Pin(13, Pin.OUT)

# ===================== Botões =========================
btnA = Pin(5, Pin.IN, Pin.PULL_UP)
btnB = Pin(6, Pin.IN, Pin.PULL_UP)
btnC = Pin(10, Pin.IN, Pin.PULL_UP)

# Estados dos botões
lastA = btnA.value()
lastB = btnB.value() 
lastC = btnC.value()

# ===================== OLED ======================
oled = None
use_oled = False

def init_oled():
    global oled, use_oled
    try:
        i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
        import ssd1306
        oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        oled.fill(0)
        oled.text("Cores Corrigidas", 0, 0)
        oled.text("A-Verm B-Azul", 0, 16)
        oled.text("C-Verde", 0, 32)
        oled.show()
        use_oled = True
        return True
    except:
        return False

init_oled()

def oled_show_latency(latency_us, button):
    global oled, use_oled
    if not use_oled or oled is None:
        return
    try:
        oled.fill(0)
        oled.text("Botao: {}".format(button), 0, 0)
        oled.text("Latencia:", 0, 16)
        if latency_us < 1000:
            oled.text("{} us".format(latency_us), 0, 32)
        else:
            oled.text("{:.1f} ms".format(latency_us/1000), 0, 32)
        oled.text("Piscando: SIM", 0, 48)
        oled.show()
    except:
        pass

# ===================== Variáveis =====================
DEBOUNCE_MS = 50
current_latency = 0
last_button = "Nenhum"
active_led = None
led_state = False
last_blink_time = 0
blink_interval = 500

# ===================== Laço principal =====================
last_update_time = time.ticks_ms()

# Desliga todos os LEDs no início
led_red.off()
led_green.off()
led_blue.off()

while True:
    now = time.ticks_ms()
    
    # ---- Controle do piscar do LED ativo ----
    if active_led and time.ticks_diff(now, last_blink_time) >= blink_interval:
        led_state = not led_state
        
        # Controla apenas o LED ativo
        if active_led == 'red':
            led_red.value(led_state)
            led_green.off()  # Garante que os outros estão off
            led_blue.off()
        elif active_led == 'green':
            led_green.value(led_state)
            led_red.off()
            led_blue.off()
        elif active_led == 'blue':
            led_blue.value(led_state)
            led_red.off()
            led_green.off()
        
        last_blink_time = now
    
    # ---- Botão A: Vermelho ----
    a = btnA.value()
    if lastA == 1 and a == 0:
        press_time = time.ticks_us()
        
        active_led = 'red'
        led_state = True
        led_red.on()
        led_green.off()  # Desliga outros LEDs
        led_blue.off()
        last_blink_time = now
        
        action_time = time.ticks_us()
        current_latency = action_time - press_time
        last_button = "A"
    
    lastA = a
    
    # ---- Botão B: Azul ----
    b = btnB.value()
    if lastB == 1 and b == 0:
        press_time = time.ticks_us()
        
        active_led = 'blue'
        led_state = True
        led_blue.on()
        led_red.off()
        led_green.off()
        last_blink_time = now
        
        action_time = time.ticks_us()
        current_latency = action_time - press_time
        last_button = "B"
    
    lastB = b
    
    # ---- Botão C: Verde ----
    c = btnC.value()
    if lastC == 1 and c == 0:
        press_time = time.ticks_us()
        
        active_led = 'green'
        led_state = True
        led_green.on()
        led_red.off()
        led_blue.off()
        last_blink_time = now
        
        action_time = time.ticks_us()
        current_latency = action_time - press_time
        last_button = "C"
    
    lastC = c
    
    # ---- Atualização do display ----
    if time.ticks_diff(now, last_update_time) >= 100:
        oled_show_latency(current_latency, last_button)
        last_update_time = now
    
    time.sleep_ms(10)
