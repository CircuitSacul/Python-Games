def create_board(character_list, boardYsize, boardXsize):
    print ''
    for l in range(0, boardXsize + 1):
        print '_',
    print '_'
    for i in range(0, boardYsize):
        print '|',
        for j in range(0, boardXsize):
            for character in character_list:
                if character['x_position'] == int(j) and character['y_position'] == int(i):
                    print '\b'*3,
                    print character['marker'],
            print ' ',
        print '|'
    for i in range(0, boardXsize + 1):
        print '_',
    print '_'
