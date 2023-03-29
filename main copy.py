import ctypes
import threading
import time
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk

import keyboard
from ttkbootstrap import Style


class Application:
    def __init__(self):
        self.current_slot = 1
        # (元素, 継続時間, クールタイム, 差分)
        self.slot1_property = ("Alhaitham", "dendro", 12, 18, 6)
        self.slot2_property = ("Fischl", "electro", 10, 25, 15)
        self.slot3_property = ("Xingqiu", "hydro", 15, 21, 6)
        self.slot4_property = ("Barbara", "hydro", 15, 32, 17)
        self.slot1_active = True
        self.slot2_active = True
        self.slot3_active = True
        self.slot4_active = True
        self.color = {
            "geo": ("#B2881A", "#E6B322"),
            "pyro": ("#CC4733", "#FF6F63"),
            "anemo": ("#2DB2A2", "#4CD9C8"),
            "cyro": ("#55B9F2", "#73CCFF"),
            "hydro": ("#1C80BA", "#4C92EA"),
            "electro": ("#AA50E5", "#C773FF"),
            "dendro": ("#39B100", "#7AD84C"),
        }
        self.icondata = {
            "geo": """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAFIElEQVRIDbXBf1DX
9R3A8efr/QEEv/4gbOFxAg4m69C1E8EhWrtCDUWn3lX+dmsKlTJzWz929uPKYWfa
rFT8iV6y2PQyD5uiktICc6FDTW+mAzFtIDoldJjG9/t5v4bf+l6SoPSHj4dwmwm3
mfB9PJyJmpBNf2umw4QOMsyZQJM64ep4HV1W6HXpEKEDKooGl5dUIs1P5Vlg4axQ
o9ybEPqzOY3cinArtTvSSz/4WMSZsuAS35D1f+hslKjuXdPn1nNTwk2d/zBzX1m5
tRqWtjl92DACVua9Hn3+JVoYyXyhkfYJ7asre+D0Pyp9BhIn3Ze5wtJKxZIu3q+C
wXel2Qx77iLtENrx3/0ja/futYKqSX6yQWHzxvVx9b+xYpJmN+JX+WZEsFqfmKrz
l8f/8SvaIrSlcf/M2v0bRWnxk5wLrvL55pRLddUE9M35AjBweGk3EQcorm58+g3l
BkIbnOrl4T5RUTxRMTFjD53bMuhC7XGu4xpJfPwCsCT36Qcj1uKXf6DvovxyWhPa
Ur02Cr8fTa87uiY6xLhW6OTxxE6oQqheEwWcuuJJz6kCqlb/QJxgVQtMzIv+58H9
XEdoreFfEyP6/vXkn+NcUaOohDj4rPByyeD1BQUoLf6S/6fUTksRmZEfXfr3MhMs
1et6KxhFhbipn4OPAOE6OWOCXn5hTI/kd48dei30+FtiXFpoUOwjR4CaVbGelOTI
pHeBo+uiPV3CrfX9cMKnQMFT5r6BCVYwSsOVkKRfHiZACAj39Ph3SSrwVsG2Z1Zx
uijJGHGF2F9Uopwte1CcIOCuIdtQBP6zZYArFB0eOvv5V0XkVNFPUSNghSeWhRW/
/xF+QkD97gylWZQWPYeWNux9tPl/J3pmlGVlTc99pEaNI0pc5p7LV68CZ4pT1QQD
0SPKVbHwxsw7x4+62wotFNNrxB6wgBBQt32woICoKXzv4O9XXjZg4UzxEFCQqJF7
lGvOlQ5XQdC70ndh9XTxkIg74roMKji7ezhY/CLTd+EnBIwZmbI02zVcYyFm7AHg
meyHZo86qVZjxh1UdF7uvFk/r3DFWHF7phUbOPnegCBFVXuNPTA/S7J+NdKoGT+3
cXdZOX7CdY5tSAlzmowaK+ysOJ79mg84taGfim26dLFfVi1w5tCYL/cdic+uQfhs
492AKCrY+Clxyc837HvoxUWblr0DyteE1k68HYdao1gx8dNqUHJfXDA5YbUin1x9
dtyMbK4x298v+fHZx8CnGuJgFaxx4yd/du7IlMh7ClWVAKG1yZOmvjSsVFxBrFr6
ZNUBH6yIig6hRcYrodUnak4VJnivXgKjTtDp2LWxNVNBREz8r2u5gXCDyDA+XByB
IrC9bvqc3EVA1YquVh0wBHhiEnqN+rimKNFbV49f08BdA5KTaE1oy8JZMioxAr/E
WRfw+3R5D1W+FhzTu8/oSjDHlkdYVaBz2pDeSVtQvkNoR+Fcp1/Pbkbx4iQ9eR6/
T5aGq8rh8MXTpj0KVObdGeRzEWIGDb4jZSttEdq3Y1637mEGCPWE9p9ZDzjgCigt
jm793cVj+RZzT1pq17QdtEO4qe253Y2iQnXkwpysx/iWKZnfxTV2YOr9Pe7fxjWW
tgi3snNB9y+arFE7fv5l5RsbnvMYZcCI/vH3fgRK+4QOKM/rfKRKrUrOm18Cq37b
yVWTkjEtJWMVtyJ0zNurX6+qeNaLLwzHq/Qf/c64cWPpAOH7mPFwCOrN36R0mHCb
CbfZ/wG5OxY/HJMIXAAAAABJRU5ErkJggg==""",
            "dendro": """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAEyUlEQVRIDbXBfVDT
dRwH8PfnOyYoaWQgKgIG6BgwwICOuiZGpohPaSimEXg+pT2Yp+0UkkorNDw1nxD0
pFASr8wkL/TEQk5OExEcDwPFRBAUMPJOTXTb7xPO5rEE+/kHrxehhxF6GOFJfFnl
5WT/1CJvPWQjyJb66brU0GwALa+XwgSZCLL55I0wggWjw6XoMshDkM3/2Ah0YAGS
Kl8thTwEeQQQWqBhCFiUjDonQRaCxZwFbxcF1mkb/Heu2c5gdEVbqGEFK83CLFCo
1YPRpQ+TFhd5FYeWh6Rt3AyAYOG59RW/kD9xH+eFVwAMwHWQa+yPLkKpCLmsi3tj
FoCo3wMES7+EGwD+4egWg1ua8d4Q79IZ8bNnAyCIMSdVguwlwsVqqTZeD4BgMT1u
pmmxHiwAtDSI8/ObXsobIEAASYQOghHponxvaAkgctoC9l5ksEAHkgTDLHB6fGtY
Zn87Z4VE6HAwrBwWBCu3TE1EsADQUN/uPkRJpHC4RdrmjxOmxezbm503/It7Qjl2
IDspFTn1Rqn9bkLb2nETpmbu2lHmu7PF4Q6Amy3o6yIAVJyn8jdLYUGwtTLpo8bp
RxgiM6gMFkTEzAAWnvUrmKUwVJfHF/vuDq2WYCOhTCOIMoP0TADjIYKtuZUaJXNj
ok9u7k8x+Spn114sGECf40EbFmXjAaKE9fG9XztjJlIwuN24PbQ6etJ495Q6s+Sw
U1OCTgi2Pqjyg6nfpsBTURvHDR9bj/uEwmSurxq0P/YYrKKyx7gPa+ztSACY0FoU
lDMve1FFMClMW9UV6ITQiW7FcnPCwZpKv0NT9+sMGrMwAdLkW7qRoXPAeNSBwu0n
XDcw7IQQ64aVz9un7Rd8fZPvBSObYEXoRJseqY1s5t0xKas+W1L7Qm++zYQUn0p0
b0WtGhBG6rXOu7QX7JfWep8+OfhYXD6sCFYTkmJveLRGjm42Zk9KSU5J0iUr5++X
CKu8K9G95Iv+AIzfxqasSoYjkvX+p397rv/VAd+t3AULAjA34S2PT8oUxE0mx4F2
t4+fE/mTywFMKxiq8ezj68jTBxjQlW0X1C1KunpZ2hFRLQFTDvuNUKEdzg64Lhit
KaO+3rGNYPFMWniY919Ho2rW1PkDvNzToMoKD/JQBA1tA6DXPZ+zbw9sEfD5FbWQ
RNOVZ4suXz0788LaS74SRKJX1bgC7+JWp9aYEjAItlLrA5ikX0v7HJ50BhaF+UdO
qZbp3MthK7XBN8SwJXLMaFjE5YcEqv++I5mTPc6D8RDB1spEndOCQyTYtHu+LnEJ
rKbkTDww42dYvZwVdmJ2Mcx44Kv0DLvoDUxY6mmAGZ0RHjH2+/DoF28AKPmjPWtk
Hf7Pu2VePi69wKK6xCd9ci5sEbriMWfQstV9wQJA/TW79SGVEhiPWG9Q2T3NYAGI
Yr3bnvFHWcJ/ELq3uSkAMAvcd++mtERVA6u0KypJCFhIJL3vVkMSGF0gPNbSolHe
XtcAAlgw3hlcTUTbGlWEfzW2OKwOLkP3CDJsKo6wd28BQIwOTOhArcMXanLNYDwW
Qbb0a2pYLRhsgAQ5CLJ9UzHxrnMtAPe2sGi/LMhDeBIZzWrBmDvQANkITyIjY6tK
HRihjQAkyEPoYYQe9g+neNswYkgNZQAAAABJRU5ErkJggg==""",
            "hydro": """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAER0lEQVRIDbXBf4zX
BR3H8efr/fncHXGITrzSdF4bBnkD3ZjQf9ZyK6fM1ZbGih+Lc47zvNWsCS1QZsWq
zT8KEXDWRdycuba01XAu1zBXpv4hnTh1TcXWb7Uk8Li77+f96vgcB3fC1/v+w+Mh
zjJxlokWbN74re0f633nxXmMnENVMf9trm9894Wfbrp1E7MRzQn8A/Mq0xjEKS4/
R34ykqZEE/p26rBSTAg7JU4xiOMMAuasGznWM5czEacRbd4yxhkYRBNlRWObOI14
j4AtlRQOlJygBIWz0ijREVVYnM6RbCmZScykbXZQmAkZhKmiunrfNU/u3y/LNqeo
47Ec/VOGI9NI2BTjbOzAnCSm25rMNyQOBA6+JhCY93FPSpygiptKXyymiGnih5li
UowrbxetmX/AR37HSRdt+/Bf//Z3amJKB4ztTmqyckMBSW3dXffsueQrUHBKY9Po
0PcG1tumds5wdfSpcBiIi7K6oaQmpunY7rFOLPhyAUmteOA/GeeCmKDEwRSLraO/
3rphJbX2QY8LkgleL2piNtpjF4lBCSUkFgIjsKzF4eXiuGCoAcba2/bwmlWrADGb
vk1bdy27UyREKsOWiyoSIgwkBEvInmDCL4/EsTkQHVdr5EIB4qQ972pBOytL0wKp
3JcewSCwnJ8NYPDBvb1zViOy7RgrPwCISXf9T8s7w8oCXydas7D7sld3vCIwSM7r
C0C/So6TVwoQtfZ9roIJKfvTQct27byvb2EfINvXFrb1eIYl3PhMAKLW13vr7i/u
ADouYXSxkmYKqJhJw+P6Vwlsfmvf3TddVz6RDSlMXiNAtOhH47GolLGYEOfRWCom
iXjSgC6k+qiK/XZQdDN+qQDRguLpKomicoqEgATazVUFNT1tp+MC5SIVv3cGQ4cG
v/SF9YCYTdcdr711YzfHiZl+cui+tZ/vB8rh8TxW6nyqhdJzlp0rAjNBzLTs9j8e
WLMi2+wlwaQDjSJVPWUGSgSh4rlMOUzxQcYuDqB4+Z850jX/3DdoLDh8tNPtFT1t
1MRMnX/wyDwkqiWi1vZCJqqWCjOpPGibCe4iPyQgDlrmoeGHV11xI9bg8z9bu3oV
NfFeKn7T2PnG0C3r11ErX7KdvrxIThjce3/vVb2EvLg0CcTLBgYOHri350rPrfLS
kiliNvHVhgcKLxRNfPyJ55/tXjr02I/XXHszUF1WQDJFtKB83Rf8/KV/fP1yplMn
HJXhdTMKHUD6IwUziSb6+gd27thObcWy5c88+kz8diTXzqXW9orHFxVA26Gq8W6l
eYVMdodtZhJN9A/csvsbuxq/MP0FtSDykXGdF/6USDbu3Pv9G1bzb0eXijcZu1Kc
iWju/AVd/33oL7G0w6Z8E15szI23D7cvKHqKap6p6Uh17+MPbOjvownRgm9u3vad
K26LT3TiAMI0/vzO3cP339l/B+b9ibNMnGX/Bz+o1jBkgP4aAAAAAElFTkSuQmCC""",
            "cyro": """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAEmElEQVRIDbXBXUzV
ZRwH8O/veZ7//3AOcM4BFDgIgUKKr5NZtl5s0p1bN9WWbYopluTU1Wza2ipXmRct
28y2fCF8QZarm+ZN6642m9WF9jLAJSJvB0iEA+cFzjnP/3me6tRxEDr/XPj5EO4z
wlwQYDA3hLn4SkkD8TwnuEaYiyMdvcxgz/JKuEZw7XwsPTY0AqCoLLgxLxfuEFw7
1hM2xJGxs6oUBm4Q3DkZHgGwZGz8ariHVq52mN4ZKoELBBeefevNDbv3EdFLJQUA
Tt6MGGPWJeXSyhLcCyFrqL839MAiGIVZOEERNY/FDj/6cGdn5+mxxNZ5fhgFgzvh
A+Hu8gWVyCBkMeDIr93GFoJzbnNwxoWoBupDhcg4Pjpm4vGUYPk5gcaifGR8kRiP
RZVxlHGU48Ck0yotV48PrK9fjwzCNF/raP8fE5ZNEBbnjFuWEXi5MKjxn3OJFBls
9nuMxr/O3IpqY2Q6aTQp6Wipq6oKn/b4kEWY6WhXv8XFI+MjdXWrKhZWHLxy9Ynh
cHXtYmS0phwGvcljI+O7nq4bwdC2glwY/PR7xy/5hY6Su6orMA1hpjf276va9boQ
omnBPA3s3bu/7v13T9TX//Dzj19qpa/1BEIFE7l5L3CPhjmbSPz29jsffXwYwPHB
m8Yx3ceOfnjoIKYhzNIyPKpAzBZEzBYiKZSXWSsikY6iIr8xwyRzyG4QojWVttLJ
uBYCcKRUjjIwTaXzDAymIcxG7HQ8sjW3ANBE/Gpf+HJJseHGmUpZvhylpIqnLL/X
46gVN/qW1C7G3xjOjE9uDfqMxv8Q7qSnb6jqgRCyTk1NeWw7mUx4fPkacBIJn9fn
aGyyGLK6wjdrFhRjFsKddA8MLyovRVabIznYVGzCEywAlBWZkIGggdosPMYYZHQM
DiwrK8cshNmItUxEtvsDBv/outF7qaqMKUrGYl6/nwFyUnGvZYxZNTy4sqIcGa2J
VEOuF9CYiTBLcyRqUo7gnDjntqhIy/48T0NOsC0djU0lV8YSPcVFmwKBc5Ho+Dff
5j+1jjSXUmpHMZttLwxiJsJM4fDQBQ3B7R1l8w1pGGqNJxryc5nh502i7+KlZWvW
pDzsGZ7LgLPxyc15AZAEcCI8ZpTzSkXIQGEawkyfXgtzm9emIvWLl1YurHrvSvu2
YEBDAxpAWyrpEHvRtpHRNTB40ed/sKvj8bVrv+/s7PAVKCl311RgGsI0F+Ro7/VJ
bhPjlpcJaYMJq7HIj6y2eEoxbPF5kNUyNk6KTFKmILVjdErWVJdusDzIItxG+OTK
dbIEtwSzGLMEY0wX2Du8+chovjWup5JaM9srGosLkXFqcsSJci0dJR04RklHpeVr
dTXIItxm2ZBp3AUBn49OHH6yvr39cstotLEoCGjcjWVDppFBcKFp56sPHTjADLaH
CgE0/xkB8FhCLltUjHshuPPZcEQoZ9fq5XsOfVC74TkBs618PqBxLwR3OOhozyAR
AYwp1VQdgoEbBNfaEhMTg1EYlheav8Vvw8ANgnuEI+29zGDPikoYuESYi1ajbdBG
IrhGmAsGaMwN4T77C80s/jCKD1qjAAAAAElFTkSuQmCC""",
            "pyro": """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAEt0lEQVRIDbXBa0zV
ZRzA8e/vORzCA3ghvAAqmoh3AkUUhTDNS95mM1MLxbzkC23p2nJzvrCWm9as2XJN
5xWv6bLUNqdkCoKaKCokXjDRFCTwBgoe4fyfJ8POdsiOHl74+QgvmNAYGW8mD913
hMYQGiM/ImrlpFGrlq/AZ0Jj5IdHg4opvYDPBJ9lDB8Rcf6qFkJCHeGn8vCN4Cu5
0KmriFCvy+VCfCP4pqhbVxE7blGFBfhG8MGVngkidYg2ghgcQf6tj+biG8EH1+Ji
DEK9pgEvL+jTcdHFE5EZBfhAeJ4Z06YsLiwwoAxadNyl66ejI9ufKABrzuypK1el
80yCd5tDQlPv3Jo1dcanl/PAaCEy58z1Ab210PZoHoabibHtjhW4sPBO8O5mSlzl
3Zqu+RdvvhaPWMBHLTuuqLgGRGSe2pI6ddD1AiAs8zTeCV6UpfRWNhtwxGqmy0pS
IoKABeHdl5UWAkbVvURgra4FdvZ5fc6XX+CF8H8K23du1bUpKOpVlj9a3q/nZ8VF
oMCIYIwJPZB3a1gsKCD0QC5eCE+Z+8bgxfZqhQbNvwRju+JkXbM2nz8qQ1yAzfhb
dqVdtQpQam9s77Ql3/EUoaGo6I4nu7TSgs2yGWVwq7xW27espKK8zEBYeNjFHlE6
wPVTZ2tckY16WnRx+059vt1KQ0JDVWMHGNFnCiriYkJBAdeL7/U4e556dmgKt3lC
qsb1x21dQt/pJ08233Vco/EgeBg9csg2x4PmP564MzZBBJCrl5wxv59ByO8c2aFn
mIhQz1GnbHtyQO6P72+MAcpCX+m2envlhISgncfxIHioGZ+y81zdouobl/q31aLA
FbjjOJDbMiJmQKeyitutIppp4YnyFmEdV/1w7+14u/LnMaUCt2fXTE4K2nZc48JN
8FA9KTF877n71Q/uTxooRhefLO3xRzEgSowxGB77cP4Hy8oKlcESArdlAzUTBwLG
mMAdR/d+vGho5eGANdm4CW7Bwc3Kx8SE7zt7927Vw/cGYtSkKsfun/fPSktbUXdZ
ic2xJVujgdtj+jmC/YEmW48AD99N5h+qydZMZ9pblq4I3JSNm+Dh4ZQkl9MveOfh
/KgO0f3bbi6yz/ztkDM1SQyOrXmWqaHevIWLl/75i0352dMPA87UJCBg8zGwaqck
F3Xr0mPhGtwED8dadoofGT4768q64hLnhIEqCP/1OXVpyYB94xHcbo3t6wj2d2zJ
ATJmTx7kvIFW9k2ZrqkDjIh/+lFjDG5CQ7lt2sUO73D+4O2YG4W7o+O+T+iSLiVa
SZP0LMvwHwsWzl9SekohakOma9prgN+GLBoSntK9Z/eC+DZa1e0vDhh9KAMw0weD
TdZl4KFi9KshrVvErj18bGJiE4e/McZvYxZGgcaD4MWexCGjutcBLdZmVYEorvbt
065XkLE0qPK/7q7sNeaTi786WvmJJevbxM9c8hUo0DQkPFP5sPiQyCDlsi0Mj126
ZDluc+e9/03lVWzaeafGsSsX74TnEvSMFOBeiStkX45CWWkjjL0ajN+aLM1zCL4p
HZEY1j4At9NXrN4HszA8l+Czr99Jnde8BLCtztJiYfCF0Dg2lIXGd8IL9jcGFtUw
EzqETQAAAABJRU5ErkJggg==""",
            "electro": """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAEzUlEQVRIDbXBCWwU
VRwH4N9/ZnZ2d3a7XZS4BcFwhMSioIJRIUixQYWCHEVoPTBgKciVFoGgtCUUehAE
rAZKqJzhqAilFOSK4dBEE4sgMRgabahIAi2ldemxx8y898RN1mwvSkn6fYRuRuhm
hC4iUrMmbwEkR2++ojAVnSE8kty52/U6md9HPO9IqkCHCI+KQDkzijnXDW6yYCD3
xAK0h9CGApVD5+hcdLRr5bjtpjAZ001mPJvsmpGchJYILRGUS59XDv94oBAMD2HD
FxuliwOCRiDIgpzztaUpQghEILSUMXVH3tG5QjD8h46m/xgwLJKq1nivp+2aytGO
smWX/6q+FTCbgoauQ88pmYMIhAjrE3aOnzh2yIKnDn6zx3vqSbvF7VA1q9WuSpqq
2hVS/ZL/9TU90Ma22WebdZ9u+AKswWwK5pxZhDBCGAGrpu3IPpJyOf+P8oq/NdWl
WaPsVqfT4rJZHLIsgcyCa+8dKD7E0dqe1HKffs9nNifEv1B84uyYJQPjX41DCCEs
a9I2i8X6wWsTj5eXO6zuKJs7SnW77C5VcZAEgA9fJaMDBxde9QcbmoMNfSeZAxqf
PlR2PrssFSGEsKypO2wWu8PisKtOl9bTZXM7bD2cqlOSSIYgWQxdKaMDx5dUNQT/
afLfGz28T+yiQRcyrozJfR4hhJCq0opde39yWJya1amp0W57j8d7NhRcyWe6+dYz
SSPc7yuyGbtCRXsuZN4IBtVGv7fBXx8/NKZf2kBAZntNeSYBIIRkj99Kml2zRjks
rrgXhw1e7AFMRChIOXDXfTNn4wq0VLCpcGTj/OZgQ6PvrtdfOzrW0y+9P4Dg1wFr
sg0AISRzSpFV0TSrc1TssBGZ/Tg42ji3quLU9dOf7UtHWOHyb0dET+Acft3v9dV6
ffV9RzfHvTsKEQghmVOKbBaHZnUu35fIwNCemJiYqs9uE9Bscn8jM5nFrwvdIJPD
MIw6X22jr/6doucE44hACMma+pVV0WaNm9wnxYmOBfcKAKuvZeTn5SHkZPrPnsde
Mgyjzlfr89dPLxyClgghGYlFNknLOvwhoKNj3p3CnUIQiHRpjfDrfq+vbtKmvhyt
EULWvFGEKHV1ySyODqWnLT1WfPr6nd/R0i/ZvDnQMGadWwi0RQipOHC1uORidsls
RPB4YmpqqhH250Zz0FIFbXz3SeW4dYMYCOBogxCWOa0op2QuInh6xZz86HZl9feN
zDuy/2QAgz8ldBEhLGvStrXH5iGCx9Pr8JxKu0UjCRKEJNGbm2Oqq2vQFYT/SQBH
K6eW3dIsDpvqkEkmCUd+3Z1bOhtdQXigksW/qYrLpmqqbJMlRSHplbU2PNDJ+ecS
tsYjjNCZ/QsuW2W7KtskSZJlWQgkbOiD9lz5sqLk/A95pfMZGMIIncnNy+5bNZZk
RSErEQEQgt0JVKfvnkCCOPH968tuXmoKMsYM4+WZngnTJiIC4SEQsGXWGVlSJCIu
hOCCc24KxkxDFwGdmybzmxxDk1xJydPREqELlJy392mqjQvBYXJumvw+pkOHyfPL
5jESEGiF8NAkgKBkJBYpZAGEEMwQXJDRK44tSluIDhAewua0/dU3mgEQyUIwAIKx
J3r3Ti9KFMTBBTpG6GaEbvYvd+gNP/o76/gAAAAASUVORK5CYII=""",
            "anemo": """iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAEoElEQVRIDbXBW0yT
ZxwH4N///b6Wlk6QiYiSeGIqXrjFzXiMClLaQi2gSFWi0cydlzh3tSy7292yiy3b
srhDzA4qoNAVoWBLKTg8ZM5tccuCoDjnonac5NhC2+99Rz5Tg5NCveB5CDOMMMMI
U/I1tWyzZmMUk2r0ukOjinV7AWIjxJYbqtWSaNAUIjaL4uQRyZNgQwyEGCxjTpAU
kSSvVIDY8sN1YhwXbl0hJkOYzMGbTd0LAoLwto/l5VsRW2OL9+P1QQDzbs06lpWN
xxD+hwCB/KCLEca59FYITIVgDTYAHIBLZ8VjCBNUOGv3F9vCgDXoZjwCoNZgxdQI
tmEXAAHUGawYJ2sRCSGKMMGOPndi36wTz2wsHKyH6s3LGrMxD7E1+9wfrVGgOpNU
sO/GpZHU/h9m5yOKMEHRwFlOrDbJVDRwFipFQ3WJZsRmHamTIzJUNcmWogE3QDXJ
JkQRHiIU97kBHDo3+s1WPRckiANwppgRW/F9Nx4gqWG20dzvYUI4U8yIIjxE2Nnt
4YAgVjPPVOw/C1VxJx1cl4fJfNVa71opQ+VKtRV0nyEiAM5UE6IIqoKyPfUnK3b2
eKDSD2okFho2MIwj7kg143GEHV1eggCgG2NcYEwfIcEAOObm1bq8NqsRAEFV0uV1
pBlfvHGpP3lIQCbBE0aV3VfHvluXCIBx7en0LXjULr+HS0wSOPAL/34VCydAEuCA
1ItTK40lXd7qNCMAgmqXvwngVel5pXeaFTkCMCbACY50U9FgvTwis5B8euFWRNlv
N3MtH9WHjlxkR1fLnMAEOIEiVJ2xreSeh0iqSjcCgqDa6fcxkOCiOmNbxvPPbqj7
FMShUpgSeemTjvZra5zlJ1a+AGBX57k/tr/cfq1jt79REQxgADhgagu+llOw925T
mAFgVfNzIEBQldxtIYFxgvi8YPjzTDMDFi1cYm/4ojNFFkLI+kDlHBsEHtjd41PG
GCS+5L7YcjNgs9oAvHrb2ytpAAFVVUY2AIKq9FYLyZgc8cM/hT/MYfIYq07PBWC/
4wvplf3neeVqiTOZCRAg8IAACAALU8WSrQAIUfbbrQDHowTx9T3cffTbp999xfrv
kGOphodh7FYuJCWu7exTkgw/L9CCC0QJAglIHOWLcwAOgDDBoRvNQ1oGVUivHPk1
nG3OBziAk57mMrPJ/o9HIeXAldFhvVxmskDl9HiPrea6oA4QAGaPhb9cZkQUIT6f
Nft+m2uYk9IvEOoaSF3eP/jeRjPiQJjOO22Nt3R6gqjIzLUEnBKF3mo1HMvUCbDF
w4EPVuVhSoTpOBrclVmJkkDF0s32v1qZQPnSzXuunxMyK7k+UmqyYEqEabC9nb75
LPJ7Kk/363oWDWkp4am/tb3pgXX3ZnWAVyzbjCkR4nCw4/ygHHI8l/t6Z8O9BP7G
FcPXmRFNKLF8+QaOaRDiULrXrnn/sMxZcnLfoCai9KZxwskVm8AFpkOIT02tszIr
7WrhoT/b2/a1XT6+Yi0IEJgWIW52/4/6IUnhIpA27EixID6EJ1HWfoEJdjxrE8AR
H8KTyOZ1ITJcpFyAIz6EGUaYYf8BCUjkMPuZeUAAAAAASUVORK5CYII=""",
        }

        self.window()

    def window(self):
        def info(title, content):
            tkinter.messagebox.showinfo(title, content)

        def close(event):
            root.destroy()

        def slot1_pressed():
            if not self.slot1_active:
                quit()
            else:
                self.slot1_active = False
            # 継続時間
            style.configure(
                "slot1.Horizontal.TProgressbar",
                background=self.color[self.slot1_property[1]][0],
            )
            progressbar_slot1["maximum"] = self.slot1_property[2]
            progressbar_slot1["value"] = self.slot1_property[2]
            progressbar_right_edge_slot1.itemconfig(id, fill="#C3C3C3")
            for i in range(60 * self.slot1_property[2]):
                progressbar_slot1["value"] -= 1 / 60
                time.sleep(1 / 60)
            progressbar_slot1["value"] = 0
            progressbar_left_edge_slot1.itemconfig(id, fill="#C3C3C3")
            style.configure(
                "slot1.Horizontal.TProgressbar",
                background=self.color[self.slot1_property[1]][1],
            )
            progressbar_slot1["maximum"] = self.slot1_property[4]
            progressbar_left_edge_slot1.itemconfig(
                id, fill=self.color[self.slot1_property[1]][1]
            )
            # クールタイム
            for i in range(60 * self.slot1_property[4]):
                progressbar_slot1["value"] += 1 / 60
                time.sleep(1 / 60)
            progressbar_slot1["value"] = self.slot1_property[4]
            style.configure(
                "slot1.Horizontal.TProgressbar",
                background=self.color[self.slot1_property[1]][0],
            )
            progressbar_right_edge_slot1.itemconfig(
                id, fill=self.color[self.slot1_property[1]][0]
            )
            progressbar_left_edge_slot1.itemconfig(
                id, fill=self.color[self.slot1_property[1]][0]
            )
            self.slot1_active = True

        def func1():
            threading.Thread(target=slot1_pressed).start()

        def slot2_pressed():
            if not self.slot2_active:
                quit()
            else:
                self.slot2_active = False
            style.configure(
                "slot2.Horizontal.TProgressbar",
                background=self.color[self.slot2_property[1]][0],
            )
            progressbar_slot2["maximum"] = self.slot2_property[2]
            progressbar_slot2["value"] = self.slot2_property[2]
            progressbar_right_edge_slot2.itemconfig(id, fill="#C3C3C3")
            for i in range(60 * self.slot2_property[2]):
                progressbar_slot2["value"] -= 1 / 60
                time.sleep(1 / 60)
            progressbar_slot2["value"] = 0
            progressbar_left_edge_slot2.itemconfig(id, fill="#C3C3C3")
            style.configure(
                "slot2.Horizontal.TProgressbar",
                background=self.color[self.slot2_property[1]][1],
            )
            progressbar_slot2["maximum"] = self.slot2_property[4]
            progressbar_left_edge_slot2.itemconfig(
                id, fill=self.color[self.slot2_property[1]][1]
            )
            for i in range(60 * self.slot2_property[4]):
                progressbar_slot2["value"] += 1 / 60
                time.sleep(1 / 60)
            progressbar_slot2["value"] = self.slot2_property[4]
            style.configure(
                "slot2.Horizontal.TProgressbar",
                background=self.color[self.slot2_property[1]][0],
            )
            progressbar_right_edge_slot2.itemconfig(
                id, fill=self.color[self.slot2_property[1]][0]
            )
            progressbar_left_edge_slot2.itemconfig(
                id, fill=self.color[self.slot2_property[1]][0]
            )
            self.slot2_active = True

        def func2():
            threading.Thread(target=slot2_pressed).start()

        def slot3_pressed():
            if not self.slot3_active:
                quit()
            else:
                self.slot3_active = False
            style.configure(
                "slot3.Horizontal.TProgressbar",
                background=self.color[self.slot3_property[1]][0],
            )
            progressbar_slot3["maximum"] = self.slot3_property[2]
            progressbar_slot3["value"] = self.slot3_property[2]
            progressbar_right_edge_slot3.itemconfig(id, fill="#C3C3C3")
            for i in range(60 * self.slot3_property[2]):
                progressbar_slot3["value"] -= 1 / 60
                time.sleep(1 / 60)
            progressbar_slot3["value"] = 0
            progressbar_left_edge_slot3.itemconfig(id, fill="#C3C3C3")
            style.configure(
                "slot3.Horizontal.TProgressbar",
                background=self.color[self.slot3_property[1]][1],
            )
            progressbar_slot3["maximum"] = self.slot3_property[4]
            progressbar_left_edge_slot3.itemconfig(
                id, fill=self.color[self.slot3_property[1]][1]
            )
            for i in range(60 * self.slot3_property[4]):
                progressbar_slot3["value"] += 1 / 60
                time.sleep(1 / 60)
            progressbar_slot3["value"] = self.slot3_property[4]
            style.configure(
                "slot3.Horizontal.TProgressbar",
                background=self.color[self.slot3_property[1]][0],
            )
            progressbar_right_edge_slot3.itemconfig(
                id, fill=self.color[self.slot3_property[1]][0]
            )
            progressbar_left_edge_slot3.itemconfig(
                id, fill=self.color[self.slot3_property[1]][0]
            )
            self.slot3_active = True

        def func3():
            threading.Thread(target=slot3_pressed).start()

        def slot4_pressed():
            if not self.slot4_active:
                quit()
            else:
                self.slot4_active = False
            style.configure(
                "slot4.Horizontal.TProgressbar",
                background=self.color[self.slot4_property[1]][0],
            )
            progressbar_slot4["maximum"] = self.slot4_property[2]
            progressbar_slot4["value"] = self.slot4_property[2]
            progressbar_right_edge_slot4.itemconfig(id, fill="#C3C3C3")
            for i in range(60 * self.slot4_property[2]):
                progressbar_slot4["value"] -= 1 / 60
                time.sleep(1 / 60)
            progressbar_slot4["value"] = 0
            progressbar_left_edge_slot4.itemconfig(id, fill="#C3C3C3")
            style.configure(
                "slot4.Horizontal.TProgressbar",
                background=self.color[self.slot4_property[1]][1],
            )
            progressbar_slot4["maximum"] = self.slot4_property[4]
            progressbar_left_edge_slot4.itemconfig(
                id, fill=self.color[self.slot4_property[1]][1]
            )
            for i in range(60 * self.slot4_property[4]):
                progressbar_slot4["value"] += 1 / 60
                time.sleep(1 / 60)
            progressbar_slot4["value"] = self.slot4_property[4]
            style.configure(
                "slot4.Horizontal.TProgressbar",
                background=self.color[self.slot4_property[1]][0],
            )
            progressbar_right_edge_slot4.itemconfig(
                id, fill=self.color[self.slot4_property[1]][0]
            )
            progressbar_left_edge_slot4.itemconfig(
                id, fill=self.color[self.slot4_property[1]][0]
            )
            self.slot4_active = True

        def func4():
            threading.Thread(target=slot4_pressed).start()

        def keylogger():
            key_pressed = False
            while True:
                if keyboard.is_pressed("1"):
                    self.current_slot = 1
                elif keyboard.is_pressed("2"):
                    self.current_slot = 2
                elif keyboard.is_pressed("3"):
                    self.current_slot = 3
                elif keyboard.is_pressed("4"):
                    self.current_slot = 4
                else:
                    pass
                # print(self.current_slot)
                if keyboard.is_pressed("e"):
                    key_pressed = True
                else:
                    pass
                if key_pressed and not keyboard.is_pressed("e"):
                    if self.current_slot == 1:
                        func1()
                        key_pressed = False
                    elif self.current_slot == 2:
                        func2()
                        key_pressed = False
                    elif self.current_slot == 3:
                        func3()
                        key_pressed = False
                    elif self.current_slot == 4:
                        func4()
                        key_pressed = False
                    else:
                        pass
                time.sleep(20 / 1000)

        style = Style()
        style.configure("slot1.Horizontal.TProgressbar", troughcolor="#C3C3C3")
        style.configure("slot2.Horizontal.TProgressbar", troughcolor="#C3C3C3")
        style.configure("slot3.Horizontal.TProgressbar", troughcolor="#C3C3C3")
        style.configure("slot4.Horizontal.TProgressbar", troughcolor="#C3C3C3")

        root = style.master
        root.title("Elemental Skill Timer")
        root.geometry("+1605+245")
        root.resizable(False, False)
        root.attributes("-topmost", True)
        root.wm_attributes("-transparentcolor", "white")
        root.overrideredirect(True)

        iconimage = {
            "geo": tkinter.PhotoImage(data=self.icondata["geo"]),
            "dendro": tkinter.PhotoImage(data=self.icondata["dendro"]),
            "hydro": tkinter.PhotoImage(data=self.icondata["hydro"]),
            "cyro": tkinter.PhotoImage(data=self.icondata["cyro"]),
            "pyro": tkinter.PhotoImage(data=self.icondata["pyro"]),
            "electro": tkinter.PhotoImage(data=self.icondata["electro"]),
            "anemo": tkinter.PhotoImage(data=self.icondata["anemo"]),
        }

        inner = ttk.Frame(root)
        inner.grid(column=0, row=0, ipadx=0, ipady=0, padx=20, pady=20)

        column0 = tkinter.Canvas(inner, width=30, height=0)
        column0.grid(column=0, row=0, ipadx=0, ipady=0, padx=0, pady=0)
        column1 = tkinter.Canvas(inner, width=200, height=0)
        column1.grid(column=1, row=0, ipadx=0, ipady=0, padx=0, pady=0)

        """
        icon_slot1 = ttk.Label(inner, image=iconimage[self.slot1_property[1]])
        icon_slot1.grid(column=0, row=1)
        icon_slot2 = ttk.Label(inner, image=iconimage[self.slot2_property[1]])
        icon_slot2.grid(column=0, row=2)
        icon_slot3 = ttk.Label(inner, image=iconimage[self.slot3_property[1]])
        icon_slot3.grid(column=0, row=3)
        icon_slot4 = ttk.Label(inner, image=iconimage[self.slot4_property[1]])
        icon_slot4.grid(column=0, row=4)
        """

        progressbar_left_edge_slot1 = tkinter.Canvas(
            inner, width=10, height=13
        )
        progressbar_left_edge_slot1.grid(
            column=0, row=1, sticky=tkinter.E, ipadx=0, ipady=0, padx=0, pady=0
        )
        id = progressbar_left_edge_slot1.create_polygon(
            0, 7, 10, 13, 10, 0, fill=self.color[self.slot1_property[1]][0]
        )
        progressbar_right_edge_slot1 = tkinter.Canvas(
            inner, width=10, height=13
        )
        progressbar_right_edge_slot1.grid(
            column=2, row=1, sticky=tkinter.W, ipadx=0, ipady=0, padx=0, pady=0
        )
        id = progressbar_right_edge_slot1.create_polygon(
            0, 0, 0, 13, 10, 7, fill=self.color[self.slot1_property[1]][0]
        )

        progressbar_left_edge_slot2 = tkinter.Canvas(
            inner, width=10, height=13
        )
        progressbar_left_edge_slot2.grid(
            column=0, row=2, sticky=tkinter.E, ipadx=0, ipady=0, padx=0, pady=0
        )
        id = progressbar_left_edge_slot2.create_polygon(
            0, 7, 10, 13, 10, 0, fill=self.color[self.slot2_property[1]][0]
        )
        progressbar_right_edge_slot2 = tkinter.Canvas(
            inner, width=10, height=13
        )
        progressbar_right_edge_slot2.grid(
            column=2, row=2, sticky=tkinter.W, ipadx=0, ipady=0, padx=0, pady=0
        )
        id = progressbar_right_edge_slot2.create_polygon(
            0, 0, 0, 13, 10, 7, fill=self.color[self.slot2_property[1]][0]
        )

        progressbar_left_edge_slot3 = tkinter.Canvas(
            inner, width=10, height=13
        )
        progressbar_left_edge_slot3.grid(
            column=0, row=3, sticky=tkinter.E, ipadx=0, ipady=0, padx=0, pady=0
        )
        id = progressbar_left_edge_slot3.create_polygon(
            0, 7, 10, 13, 10, 0, fill=self.color[self.slot3_property[1]][0]
        )
        progressbar_right_edge_slot3 = tkinter.Canvas(
            inner, width=10, height=13
        )
        progressbar_right_edge_slot3.grid(
            column=2, row=3, sticky=tkinter.W, ipadx=0, ipady=0, padx=0, pady=0
        )
        id = progressbar_right_edge_slot3.create_polygon(
            0, 0, 0, 13, 10, 7, fill=self.color[self.slot3_property[1]][0]
        )

        progressbar_left_edge_slot4 = tkinter.Canvas(
            inner, width=10, height=13
        )
        progressbar_left_edge_slot4.grid(
            column=0, row=4, sticky=tkinter.E, ipadx=0, ipady=0, padx=0, pady=0
        )
        id = progressbar_left_edge_slot4.create_polygon(
            0, 7, 10, 13, 10, 0, fill=self.color[self.slot4_property[1]][0]
        )
        progressbar_right_edge_slot4 = tkinter.Canvas(
            inner, width=10, height=13
        )
        progressbar_right_edge_slot4.grid(
            column=2, row=4, sticky=tkinter.W, ipadx=0, ipady=0, padx=0, pady=0
        )
        id = progressbar_right_edge_slot4.create_polygon(
            0, 0, 0, 13, 10, 7, fill=self.color[self.slot4_property[1]][0]
        )

        progressbar_slot1 = ttk.Progressbar(
            inner,
            length=0,
            mode="determinate",
            style="slot1.Horizontal.TProgressbar",
        )
        progressbar_slot1.grid(
            column=1,
            row=1,
            columnspan=1,
            sticky=tkinter.NSEW,
            ipadx=0,
            ipady=0,
            padx=0,
            pady=42,
        )
        progressbar_slot1["maximum"] = 1
        progressbar_slot1["value"] = 1
        style.configure(
            "slot1.Horizontal.TProgressbar",
            background=self.color[self.slot1_property[1]][0],
        )

        progressbar_slot2 = ttk.Progressbar(
            inner,
            length=0,
            mode="determinate",
            style="slot2.Horizontal.TProgressbar",
        )
        progressbar_slot2.grid(
            column=1,
            row=2,
            columnspan=1,
            sticky=tkinter.NSEW,
            ipadx=0,
            ipady=0,
            padx=0,
            pady=42,
        )
        progressbar_slot2["maximum"] = 1
        progressbar_slot2["value"] = 1
        style.configure(
            "slot2.Horizontal.TProgressbar",
            background=self.color[self.slot2_property[1]][0],
        )

        progressbar_slot3 = ttk.Progressbar(
            inner,
            length=0,
            mode="determinate",
            style="slot3.Horizontal.TProgressbar",
        )
        progressbar_slot3.grid(
            column=1,
            row=3,
            columnspan=1,
            sticky=tkinter.NSEW,
            ipadx=0,
            ipady=0,
            padx=0,
            pady=42,
        )
        style.configure(
            "slot3.Horizontal.TProgressbar",
            background=self.color[self.slot3_property[1]][0],
        )
        progressbar_slot3["maximum"] = 1
        progressbar_slot3["value"] = 1

        progressbar_slot4 = ttk.Progressbar(
            inner,
            length=0,
            mode="determinate",
            style="slot4.Horizontal.TProgressbar",
        )
        progressbar_slot4.grid(
            column=1,
            row=4,
            columnspan=1,
            sticky=tkinter.NSEW,
            ipadx=0,
            ipady=0,
            padx=0,
            pady=42,
        )
        progressbar_slot4["maximum"] = 1
        progressbar_slot4["value"] = 1
        style.configure(
            "slot4.Horizontal.TProgressbar",
            background=self.color[self.slot4_property[1]][0],
        )

        threading.Thread(target=keylogger).start()

        root.bind("<Escape>", close)
        root.mainloop()


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    Application()
