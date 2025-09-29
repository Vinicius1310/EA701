#ifndef SSD1306_H
#define SSD1306_H

#include "hardware/i2c.h"
#include <stdbool.h>
#include <stdint.h>

typedef struct {
    uint8_t width;
    uint8_t height;
    uint8_t buffer[1024]; // até 128x64 = 1024 bytes
    bool invert;
    uint8_t address;
    i2c_inst_t *i2c;
} ssd1306_t;

// Inicialização
void ssd1306_init(ssd1306_t *disp, uint8_t width, uint8_t height,
                  bool invert, uint8_t address, i2c_inst_t *i2c);

// Desenha string
void ssd1306_draw_string(ssd1306_t *disp, uint8_t x, uint8_t y,
                         uint8_t scale, const char *str);

// Mostra buffer no display
void ssd1306_display(ssd1306_t *disp);

// Limpa buffer
void ssd1306_clear(ssd1306_t *disp);

#endif

