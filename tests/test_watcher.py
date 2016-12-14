from future.utils import with_metaclass
from acceptanceutils.watcher import SubClassWatcher


class Watched(with_metaclass(SubClassWatcher, object)):
    pass


def test_print_output(capsys):

    class WatchMe(Watched):
        pass
    out, err = capsys.readouterr()
    print(out, err)

    assert "WatchMe" in out
    assert "Watched" in out

    class WatchMeTwice(WatchMe):
        pass
    out, err = capsys.readouterr()
    print(out, err)

    assert "WatchMeTwice" in out
    assert "WatchMe" in out
