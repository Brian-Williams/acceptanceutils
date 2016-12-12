from acceptanceutils import surjection

one = ([1], 1)
two = ([1, 2], 2)
three = ([1, 2, 3], 3)
three_none = (three[0], None)
three_item_group = (one, two, three, three_none)


class TestSurjectiveOptions(object):
    three_lis = surjection.surjective_options(*three_item_group)

    def test_number_of_lists_returned(self):
        assert len(type(self).three_lis) == 3

    def test_defaults(self):
        for _ in range(10):
            # get a new list every iteration so can't use class attributes
            lis = surjection.surjective_options(*three_item_group)
            for li in lis[1:]:
                assert li[0] == one[1]
            for li in lis[2:]:
                assert li[1] == two[1]
