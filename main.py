from cake_drawer import CakeDrawer
from cake import Cake

if __name__ == '__main__':
    num_of_cakes = 7
    cake_drawer = CakeDrawer()
    cakes: list[list[Cake]] = [[]]*num_of_cakes
    for i in range(num_of_cakes):
        cakes[i] = [
            Cake(1, 1, (0, 1.5 * i)),
            Cake(2, 1, (2, 1.5 * i)),
            Cake(5, 1, (5, 1.5 * i))
        ]
    for i in range(num_of_cakes):
        for j in range(len(cakes[0])):
            number_of_slices = 3+i*2
            cakes[i][j].slice(number_of_slices)
            cake_drawer.plot(cakes[i][j].get_vertices())
            cake_drawer.plot_multiple(cakes[i][j].get_slice_vertices())
            cake_drawer.add_text(-0.9, (1.5*i + 0.4), f'n={number_of_slices}')
    cake_drawer.add_text(0, 10.1, "1:1 cake")
    cake_drawer.add_text(2, 10.1, "2:1 cake")
    cake_drawer.add_text(5, 10.1, "5:1 cake")
    cake_drawer.set_scale(0, 10, 0, 10)
    cake_drawer.show_plot()