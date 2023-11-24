# Reference: https://realpython.com/python-iterators-iterables/
#https://www.w3schools.com/python/python_iterators.asp 


class MyNumbers:
  def __iter__(self):
    self.a = -20
    return self

  def __next__(self):
    if self.a <= 20:
        x = self.a
        self.a += 1
        return x
    else:
        raise StopIteration

myclass = MyNumbers()

for i in myclass:
    print(i)