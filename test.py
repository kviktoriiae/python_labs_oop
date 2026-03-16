def decode(encoded: str) -> str:
    result = []
    i = 0
    while i < len(encoded):
        if i + 2 < len(encoded) and encoded[i+2] == '#':
            num = int(encoded[i:i+2])
            result.append(chr(ord('a') + num - 1))
            i += 3
        else:
            num = int(encoded[i])
            result.append(chr(ord('a') + num - 1))
            i += 1
    return ''.join(result)

def main():
    s = input().strip()
    print(repr(s))
    print(decode(s))

if __name__ == "__main__":
    main()