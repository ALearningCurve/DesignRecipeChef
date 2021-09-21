# DesignRecipeChef
Automate Racket (BSL, etc) design recipes. This tool was especially made for enumerables (which are a pain in the butt to type out)! 
View this site for yourself at [https://designchef.pythonanywhere.com/](https://designchef.pythonanywhere.com/) (If the site isn't up
just let me know)


# Usage

Can create defintions, examples, and templates for enums such as below:
With input `"A","B","C","D","F"` produces:

```lisp
; A LetterGrade is one of: 
; - "A" 
; - "B" 
; - "C" 
; - "D" 
; - "F" 

(define LETTERGRADE-A "A")
(define LETTERGRADE-B "B")
(define LETTERGRADE-C "C")
(define LETTERGRADE-D "D")
(define LETTERGRADE-F "F")

(define (lettergrade-template lg)
  (cond [(string=? lg LETTERGRADE-A) ...]
        [(string=? lg LETTERGRADE-B) ...]
        [(string=? lg LETTERGRADE-C) ...]
        [(string=? lg LETTERGRADE-D) ...]
        [(string=? lg LETTERGRADE-F) ...]))
```

Also can make a non enum datatype as well as provide alternate names for examples as shown below:

With input `1::(make-posn 1 1),2::(make-posn 0 0)` produces:
```lisp
(define COORDINATE-1 (make-posn 1 1))
(define COORDINATE-2 (make-posn 0 0))

(define (coordinate-template c)
  (... c ...))
```

# Contributing
If you want to contribute to this project or make suggestions feel free


