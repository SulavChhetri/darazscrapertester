from quantitytester.total import quantitygen

def test_quantitytester():
    #Pass case
    assert quantitygen("Wai Wai Zing Hot & Spicy Instant Noodle, 5 Packs, Free BowlS")== 5
    assert quantitygen("Maggi Veg Atta Noodles Masala 290 gm") == None
    assert quantitygen("Yashoda Foods Current Noodles Hot 'n' Spicy Chilli + Pepper 100gm Carton 20 Pieces") == 20
    assert quantitygen("Samyang Single Spicy Hot Chicken Ramen- 140gm* 5 pcs") == 5

    assert quantitygen("Current 2X Spicy Noodles (Pack of 5 X 100 gm)")== 5

    return "Passed"



if __name__ =="__main__":
    print(test_quantitytester())