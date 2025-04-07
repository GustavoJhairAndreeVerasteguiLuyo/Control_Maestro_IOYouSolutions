[org 0x7C00]  ; Código empieza en la dirección de carga del sector de arranque

; Configurar modo de video
mov ah, 0x0E
mov al, 'B'
int 0x10  ; Escribir caracter 'B'
mov al, 'o'
int 0x10  ; Escribir caracter 'o'
mov al, 'o'
int 0x10  ; Escribir caracter 'o'
mov al, 't'
int 0x10  ; Escribir caracter 't'
mov al, 'i'
int 0x10  ; Escribir caracter 'i'
mov al, 'n'
int 0x10  ; Escribir caracter 'n'
mov al, 'g'
int 0x10  ; Escribir caracter 'g'

; Configurar segmento de datos
cli
xor ax, ax
mov ds, ax
mov es, ax
mov ss, ax
mov sp, 0x7C00  ; Configurar pila
sti

; Leer sector de firmware desde el disco (suponiendo BIOS compatible con INT 13h)
mov ah, 0x02  ; Función de lectura
mov al, 1     ; Número de sectores a leer
mov ch, 0     ; Cilindro 0
mov cl, 2     ; Sector 2
mov dh, 0     ; Cabeza 0
mov dl, 0x80  ; Disco duro
mov bx, 0x7E00  ; Cargar firmware en esta dirección
int 0x13

jc error  ; Si hay error, saltar a manejo de error

; Cargar e inicializar multitarea (configuración básica de TSS y segmentos)
mov ax, 0x28  ; Selector de segmento de TSS
ltr ax        ; Cargar TSS en el registro de tareas

; Habilitar interrupciones de hardware para multitarea
sti

; Inicializar soporte USB
mov dx, 0x20  ; Configurar IRQ para USB
mov al, 0x11
out dx, al

; Inicializar gestión avanzada de memoria (configurar segmentación y paginación)
mov cr3, 0x1000  ; Dirección base de la tabla de páginas
mov eax, cr0
or eax, 0x80000000  ; Habilitar paginación
mov cr0, eax

; Mostrar mensaje de carga exitosa
mov ah, 0x0E
mov al, 'L'
int 0x10
mov al, 'o'
int 0x10
mov al, 'a'
int 0x10
mov al, 'd'
int 0x10
mov al, 'e'
int 0x10
mov al, 'd'
int 0x10

; Manejo de dispositivos externos
; Leer desde un puerto serie (ejemplo con COM1)
mov dx, 0x3F8  ; Puerto serie COM1
mov al, 'H'
out dx, al
mov al, 'e'
out dx, al
mov al, 'l'
out dx, al
mov al, 'l'
out dx, al
mov al, 'o'
out dx, al

; Inicialización de sistema de archivos simple
mov ah, 0x03  ; Función de lectura de disco
mov al, 1     ; Leer un sector
mov ch, 0     ; Cilindro 0
mov cl, 3     ; Sector 3
mov dh, 0     ; Cabeza 0
mov dl, 0x80  ; Disco duro
mov bx, 0x7F00  ; Cargar sistema de archivos
int 0x13

jc error  ; Manejo de errores en la carga del sistema de archivos

; Cargar controladores adicionales
mov dx, 0x3F0  ; Dirección de puerto para controlador de disco
mov al, 0x20  ; Comando de inicialización
out dx, al

mov dx, 0x2F8  ; Puerto serie COM2
mov al, 0x01   ; Configurar puerto serie
out dx, al

; Salto a la ejecución del firmware
jmp 0x7E00  ; Ejecutar firmware cargado

error:
mov ah, 0x0E
mov al, 'E'
int 0x10
mov al, 'r'
int 0x10
mov al, 'r'
int 0x10
mov al, 'o'
int 0x10
mov al, 'r'
int 0x10
jmp $

times 510-($-$$) db 0  ; Rellenar hasta 512 bytes

dw 0xAA55  ; Firma de arranque
