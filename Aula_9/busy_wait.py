# BitDogLab v7
from machine import Pin, I2C
import time

# ===================== Parâmetros =====================
UPDATE_MS = 250
DEBOUNCE_MS = 180

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
lastA_ts = time.ticks_ms()
lastB_ts = time.ticks_ms()
lastC_ts = time.ticks_ms()

current_led = None
led_state = False

# ===================== OLED I2C1 ======================
oled = None
use_oled = False

def init_oled():
    """Inicializa o display OLED"""
    global oled, use_oled
    try:
        i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
        import ssd1306
        oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        oled.fill(0)
        oled.text("BitDogLab v7", 0, 0)
        oled.text("Medindo...", 0, 20)
        oled.show()
        use_oled = True
        return True
    except:
        return False

# Inicializa o OLED
init_oled()

def oled_show_latency(latency_ms, frequency_hz):
    """Mostra apenas a latência no display"""
    global oled, use_oled
    
    if not use_oled or oled is None:
        return
        
    try:
        oled.fill(0)
        oled.text("Latencia:", 0, 0)
        oled.text("{} ms".format(latency_ms), 0, 16)
        oled.text("Freq: {:.3f} Hz".format(frequency_hz), 0, 32)
        oled.text("Alvo: 500 ms", 0, 48)
        oled.show()
    except:
        pass

def set_led(color):
    """Controla os LEDs"""
    led_red.off()
    led_green.off() 
    led_blue.off()
    
    if color == 'red':
        led_red.on()
    elif color == 'green':
        led_green.on()
    elif color == 'blue':
        led_blue.on()

# ===================== Laço principal =================
blink_interval = 500  # 500ms alvo
last_blink_time = time.ticks_ms()
last_update_time = time.ticks_ms()
cycle_start_time = time.ticks_ms()
measured_latency = 500
cycle_count = 0

while True:
    now = time.ticks_ms()
    current_time = now
    
    # ---- Controle preciso do piscar do LED ----
    if current_led:
        time_diff = time.ticks_diff(now, last_blink_time)
        if time_diff >= blink_interval:
            # Mede o tempo REAL deste ciclo
            actual_interval = time_diff
            measured_latency = actual_interval
            
            # Calcula frequência baseada no ciclo REAL
            frequency = 1000.0 / (actual_interval * 2)  # on + off = ciclo completo
            
            # Alterna o LED
            led_state = not led_state
            if led_state:
                set_led(current_led)
            else:
                set_led(None)
                cycle_count += 1
            
            # Reinicia o temporizador para o próximo ciclo
            last_blink_time = now
    
    # ---- Leitura dos botões ----
    a = btnA.value()
    if lastA == 1 and a == 0 and time.ticks_diff(now, lastA_ts) > DEBOUNCE_MS:
        current_led = 'red'
        led_state = True
        set_led('red')
        last_blink_time = now
        lastA_ts = now
        cycle_count = 0
        cycle_start_time = now
    lastA = a
    
    b = btnB.value()  
    if lastB == 1 and b == 0 and time.ticks_diff(now, lastB_ts) > DEBOUNCE_MS:
        current_led = 'blue'
        led_state = True
        set_led('blue')
        last_blink_time = now
        lastB_ts = now
        cycle_count = 0
        cycle_start_time = now
    lastB = b
    
    c = btnC.value()
    if lastC == 1 and c == 0 and time.ticks_diff(now, lastC_ts) > DEBOUNCE_MS:
        current_led = 'green' 
        led_state = True
        set_led('green')
        last_blink_time = now
        lastC_ts = now
        cycle_count = 0
        cycle_start_time = now
    lastC = c
    
    # ---- Atualização do display ----
    if time.ticks_diff(now, last_update_time) >= UPDATE_MS:
        # Calcula frequência baseada na latência medida
        frequency = 1000.0 / (measured_latency * 2) if measured_latency > 0 else 0
        
        # Exibe a latência REAL medida
        oled_show_latency(measured_latency, frequency)
        last_update_time = now
    
    # Pequena pausa mas sem acumular erro
    time.sleep_ms(1)  # Reduzido para melhor precisão
