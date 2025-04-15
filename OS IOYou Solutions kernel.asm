[org 0x7C00]

; -----------------------
; Mostrar mensaje "Booting"
; -----------------------
mov si, boot_msg
call print_string

; -----------------------
; Configurar segmentos y pila
; -----------------------
cli
xor ax, ax
mov ds, ax
mov es, ax
mov ss, ax
mov sp, 0x7C00
sti

; -----------------------
; Leer sector 2 (firmware) del disco
; -----------------------
mov ah, 0x02      ; Función de leer sector
mov al, 1         ; 1 sector
mov ch, 0         ; cilindro 0
mov cl, 2         ; sector 2
mov dh, 0         ; cabeza 0
mov dl, 0x80      ; disco duro
mov bx, 0x7E00    ; buffer destino
int 0x13
jc disk_error     ; si falla, salto

; -----------------------
; Inicializar multitarea (ejemplo simple)
; -----------------------
mov ax, 0x28
ltr ax
sti

; -----------------------
; Inicializar IRQs de dispositivos
; -----------------------
mov dx, 0x20
mov al, 0x11
out dx, al

; -----------------------
; Habilitar paginación
; -----------------------
mov cr3, 0x1000
mov eax, cr0
or eax, 0x80000000
mov cr0, eax

; -----------------------
; Mostrar "Loaded"
; -----------------------
mov si, loaded_msg
call print_string

; -----------------------
; Escribir a COM1 (sensor test)
; -----------------------
mov dx, 0x3F8
mov si, serial_msg
call send_serial

; -----------------------
; Cargar sistema de archivos
; -----------------------
mov ah, 0x02
mov al, 1
mov ch, 0
mov cl, 3
mov dh, 0
mov dl, 0x80
mov bx, 0x7F00
int 0x13
jc disk_error

; -----------------------
; Inicializar controladores
; -----------------------
mov dx, 0x3F0
mov al, 0x20
out dx, al

mov dx, 0x2F8
mov al, 0x01
out dx, al

; -----------------------
; Saltar al firmware
; -----------------------
jmp 0x0000:0x7E00

; -----------------------
; Manejo de errores
; -----------------------
disk_error:
mov si, error_msg
call print_string
jmp $

; -----------------------
; Función: Imprimir string con INT 10h
; -----------------------
print_string:
    lodsb
    or al, al
    jz .done
    mov ah, 0x0E
    int 0x10
    jmp print_string
.done:
    ret

; -----------------------
; Función: Enviar string a COM1
; -----------------------
send_serial:
    lodsb
    or al, al
    jz .done
    out dx, al
    jmp send_serial
.done:
    ret

; -----------------------
; Mensajes
; -----------------------
boot_msg     db 'Booting', 0
loaded_msg   db 'Loaded', 0
serial_msg   db 'Hello', 0
error_msg    db 'Error', 0

; -----------------------
; Padding + firma de arranque
; -----------------------
times 510 - ($ - $$) db 0
dw 0xAA55

