def fibonacci(n):
    if n < 1:
      return 0
    elif n == 1:
      return 1
    else:    
        return fibonacci(n - 1) + fibonacci(n - 2)

def main():
    n = int(input("Введите какой член ряда Фибоначии необходимо посчитать (целое число): "))
    print(f'{n}-й член ряда Фибоначи - {fibonacci(n)}')
    
if __name__ == '__main__':
    main()    