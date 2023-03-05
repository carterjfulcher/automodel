class IEXData():
  def __init__(self, key=None):
    if key is None:
      with open('src/.iexkey.txt', 'r') as f:
        self.key = f.read().strip()
    else: 
      self.key = key

  



