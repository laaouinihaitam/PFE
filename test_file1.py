import file1

def test_add():
  assert file1.add(7,3) == 10
  assert file1.add(7) == 9
  assert file1.add(5) == 7

def test_product():
  assert file1.product(5,5) == 25
  assert file1.product(5)  == 10
  assert file1.product(7) == 14
