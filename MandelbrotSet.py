from main import *
from PIL import Image, ImageDraw
from collections import defaultdict

#funkcia, ktorá nám vráti počet iterácií pre daný bod
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z * z + c
        n += 1
    if n == MAX_ITER:
        return MAX_ITER
    return n

def runMandelbrot():

    """ slovník, do kt. ukladáme počty bodov s rovnakými iteráciami
     kľúč: počet iterácií, hodnota: počet bodov(pixelov)
     ak pridáme hodnotu s indexom, kt.  už neie je použitý,
     implicitne sa nastaví 0
    """
    histogram = defaultdict(lambda: 0)

    """ slovník, do kt. uložíme súradnice bodu a k nemu počet iterácií
        kľúč: súradnice bodu, hodnota: počet iterácií     
    """
    values = {}

   # cyklus for, kt. iteruje plochu obrázku a plní histogram
    for x in range(0, SIRKA):
        for y in range(0, DLZKA):
            # premena pixelov na karteziánske koordináty
            c = complex(RE_START + (x / SIRKA) * (RE_END - RE_START),
                        IM_START + (y / DLZKA) * (IM_END - IM_START))

            # počítanie počtu iterácií pre daný bod
            m = mandelbrot(c)
            #ukladanie hodnôt do slovníka
            values[(x, y)] = m
            # ak sú iter. < MAX_ITER, pridajú sa do histogramu
            if m < MAX_ITER:
                histogram[m] += 1


    # vypočíta sa celkový počet zafarbených bodov(rozsah štat.súboru)
    total = sum(histogram.values())
    print(histogram)

    # paleta, sem sa ku každej iterácii(index poľa), uloží daný odtieň
    hues = []
    # hodnota odtieňu(pre 0 iterácií to bude 0, pre MAX_ITER 1, pri ostatných sčítame ich relatívne početnosti)
    h = 0
   # cyklus prechádza jednotlivé iter.
    for i in range(MAX_ITER):
        # k hodnote predchádzajúceho odtieňa sa pridá  hodnota nového odtieňa(rel. poč)
        h += histogram[i] / total
        hues.append(h)
    # nakoniec sa pridá odtieň pre MAX_ITER
    hues.append(1)

    # vytvorí sa objekt obrázok
    im = Image.new('HSV', (SIRKA, DLZKA), (0, 0, 0))
   # vytvorí sa objekt, kt. nám bude kresliť obrázok
    draw = ImageDraw.Draw(im)

  #kresliaci cylus, prechádza pixely a farbí ich:
    for x in range(0, SIRKA):
        for y in range(0, DLZKA):
            m = values[(x, y)]

            # miešame odtiene z palety hues
            hue = 255 - int(255 * hues[m])
            # nastavíme sýtosť
            saturation = 255
            # jas nastavíme na max, ak sa m=MAX_ITER(body v množine), nastaví sa 0 (čierna)
            value = 255 if m < MAX_ITER else 0
            # hodnoty pošleme do objektu
            draw.point([x, y], (hue, saturation, value))

    # uložíme do obrázka
    im.convert('RGB').save('output1.png', 'PNG')
