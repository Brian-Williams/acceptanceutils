from acceptanceutils import surjection
import string
import random

one = ([1], 1)
two = ([1, 2], 2)
three = ([1, 2, 3], 3)
three_none = (three[0], None)
three_item_group = (one, two, three, three_none)
ten_item_group = ([0]*10, 1)

so = surjection.surjective_options


class TestSurjectiveOptions(object):
    three_lis = list(so(*three_item_group))

    def test_number_of_lists_returned(self):
        assert len(type(self).three_lis) == 3

    def test_default(self):
        alphabet = (list(string.ascii_lowercase), None)
        alphabet_plus_one = (list(string.ascii_lowercase + 'a'), None)

        lis = list(so(alphabet, alphabet_plus_one))

        final_list = lis[len(alphabet_plus_one[0])-1]
        alphabet_default = alphabet[1]
        assert final_list[0] == alphabet_default

    def test_defaults(self):
        for _ in range(10):
            # get a new list every iteration so can't use class attributes
            lis = list(so(*three_item_group))
            for li in lis[1:]:
                assert li[0] == one[1]
            for li in lis[2:]:
                assert li[1] == two[1]

    def test_static_item_location(self):
        true_first = ((True, False), True)
        false_first = ((False, True), True)

        lis = list(so(true_first, false_first, shuffle=True))
        for i, li in enumerate(lis):
            assert li[0] == true_first[0][i]
            assert li[1] == false_first[0][i]

    def test_partial_shuffling(self):
        size = 1000
        big_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

        shuffle_list = (list(big_string), None)
        no_shuffle_tuple = (tuple(big_string), None)

        assert so(shuffle_list, shuffle=True) != so(no_shuffle_tuple, shuffle=True)
