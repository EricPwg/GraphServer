from threading import Thread

from app import main
import DAI

t_bao2 = Thread(target=DAI.bao2)
t_bao3 = Thread(target=DAI.bao3)

t_bao2.daemon = True
t_bao3.daemon = True

t_bao2.start()
t_bao3.start()

main()
