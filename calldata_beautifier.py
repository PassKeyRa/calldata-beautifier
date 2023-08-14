import argparse
from colorama import Fore, Back, Style, init
init(autoreset=True)

def try_array(msg_data, slot):
    try:
        index = int(slot.hex(), 16)
        if index > 1024 * 32:
            return False, []
        length = int(msg_data[index:index+32].hex(), 16)
        if length > 512 * 32:
            return False, []
        arr = []
        ind = index + 32
        while length > 0:
            slot = msg_data[ind:ind+32]
            arr.append(ind)
            ind += 32
            length -= 32
        return True, arr
    except Exception as e:
        print('Debug', e)
    return False, []

def main():
    parser = argparse.ArgumentParser(description='Calldata beautifier')
    parser.add_argument('-i', '--infinite', action='store_true', help='Run the infinite loop')
    parser.add_argument('-b', '--bytes', action='store_true', help='Print the value in bytes for each argument found')
    args = parser.parse_args()
    while True:
        try:
            data = input(Fore.YELLOW+'Enter raw input data: '+Fore.WHITE).replace('0x', '')
            data_b = bytes.fromhex(data)
        except Exception as e:
            print(Fore.RED+'Wrong data!', e)

        selector = '0x' + data_b[:4].hex()
        data_b = data_b[4:]

        arguments = []
        arg_index = 0
        index = 0
        checked = {}
        to_print = []
        while index < len(data_b):
            slot = data_b[index:index+32]
            if index in checked:
                to_print.append([checked[index], '0x'+slot.hex(), slot])
            else:
                status, indexes = try_array(data_b, slot)
                if status:
                    l_index = int(slot.hex(), 16)
                    checked[l_index] = f'\narg{arg_index}.length'
                    for i in range(len(indexes)):
                        checked[indexes[i]] = f'arg{arg_index}[{i*32}:]'
                    to_print.append([f'arg{arg_index}[]', '0x'+slot.hex(), slot])
                else:
                    to_print.append([f'arg{arg_index}', '0x'+slot.hex(), slot])
                arg_index += 1

            index += 32
            if len(data_b)-index < 32 and len(data_b)-index != 0:
                print(Fore.RED+'Warning: wrong input data length')
                break

        print(Fore.GREEN + 'Selector\t', selector)
        max_length = 0
        for x,y,z in to_print:
            if len(x.lstrip()) > max_length:
                max_length = len(x.lstrip())

        for arg, v, v_b in to_print:
            tabs = ((max_length - len(arg.lstrip())) // 4) + 1
            if args.bytes and '[]' not in arg and '.length' not in arg:
                print(Fore.GREEN + arg+'\t'*tabs, v, v_b)
            else:
                print(Fore.GREEN + arg+'\t'*tabs, v)
        if not args.infinite:
            break

if __name__ == '__main__':
    main()
