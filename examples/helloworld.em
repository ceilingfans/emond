?+++++++%                 ; set first cell to 65, increment to match unicode for H, print char
$++++%                    ; set first cell to 96, increment to match unicode for e, print char
+++++++%%                 ; increment to match unicode for l, print char twice
+++%                      ; increment to match unicode for o, print char
!++++                     ; reset first cell to 0, increment it 4 times
[                         ; while first cell is not 0
  >+++++++++++<-          ; shift pointer right, add 11, shift pointer left and decrement
]>%                       ; once loop ended, shift pointer right and print char
<+++                      ; shift pointer left and and 3 
[                         ; while first cell is not 0
  >----<-                 ; shift pointer right add 4, shift pointer left and decrement
]>%?                      ; once loop ended, shift pointer right and print char, set cell to 65
<++++                     ; shift pointer left and add 4
[                         ; while first cell is not 0
  >+++++<-                ; shift pointer right and add 5, shift pointer left and decrement
]>++%$                    ; once loop ended, shift pointer right, add 2, print char, set cell to 96     
<+++                      ; shift pointer left, add 3
[                         ; while first cell is not 0
  >+++++<-                ; shift pointer right, add 5, shift pointer left and decrement
]>-%                      ; shift pointer right, decrement, print char
+++%                      ; add 3, print char
------%                   ; decrement 6 times, print char
$+++%!                    ; set cell to 96, add 3, print char, set cell to 0
<+++++                    ; shift pointer left, add 5
[                         ; while first cell is not 0
  >++++++<-               ; shift pointer right, add 6, shift pointer left and decrement
]>+++%!                   ; once loop ended, shift pointer right, print char, set cell to 0
^                         ; print newline
