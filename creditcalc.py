import argparse
import math


class IncorrectParametersError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise IncorrectParametersError()


def positive_number(value):
    f_num = float(value)
    if f_num < 0:
        raise argparse.ArgumentTypeError()
    return f_num


def parse_command_line():
    parser = ThrowingArgumentParser()
    parser.add_argument('--type', choices=['annuity', 'diff'], required=True)
    parser.add_argument('--payment', type=positive_number)
    parser.add_argument('--principal', type=positive_number)
    parser.add_argument('--periods', type=positive_number)
    parser.add_argument('--interest', type=positive_number, required=True)
    args = parser.parse_args()

    if args.type == 'diff'\
            and (args.payment is not None or args.principal is None or args.periods is None):
        raise IncorrectParametersError()

    if args.type == 'annuity'\
            and ((args.payment is None and args.periods is None)
                 or (args.payment is None and args.principal is None)
                 or (args.periods is None and args.principal is None)
                 or (args.payment is not None
                     and args.periods is not None
                     and args.principal is not None)):
        raise IncorrectParametersError()

    return args


def print_overpayment(value):
    print(f'\nOverpayment = {value:.0f}')


def print_differentiated_payments(principal, periods, m_interest):
    pays = []
    for period in range(1, int(periods) + 1):
        pay = principal / periods + m_interest * (principal - principal * (period - 1) / periods)
        pays.append(math.ceil(pay))
    for i in range(len(pays)):
        print(f'Month {i + 1}: paid out {pays[i]}')
    print_overpayment(sum(pays) - principal)


def print_count_of_periods(principal, payment, m_interest):
    x = payment / (payment - m_interest * principal)
    base = 1 + m_interest

    periods = math.ceil(math.log(x, base))
    years_count = math.floor(periods / 12)
    months_count = periods % 12

    y_plural = 'years' if years_count > 1 else 'year'
    m_plural = 'months' if months_count > 1 else 'month'
    years_msg = f'{years_count} {y_plural} and' if years_count > 0 else ''
    months_msg = f'{months_count} {m_plural}' if months_count > 0 else ''
    print(f'You need {years_msg} {months_msg} to repay this credit!')

    print_overpayment(payment * periods - principal)


def print_annuity_payment(principal, periods, m_interest):
    payment = principal * (m_interest
                           * math.pow(1 + m_interest, periods)
                           / (math.pow(1 + m_interest, periods) - 1))
    payment = math.ceil(payment)
    print(f'Your annuity payment = {payment}!')
    print_overpayment(payment * periods - principal)


def print_credit_principal(payment, periods, m_interest):
    principal = payment / (m_interest
                           * math.pow(1 + m_interest, periods)
                           / (math.pow(1 + m_interest, periods) - 1))
    principal = math.floor(principal)
    print(f'Your credit principal = {principal}!')
    print_overpayment(payment * periods - principal)


def main():
    try:
        args = parse_command_line()
    except IncorrectParametersError:
        print('Incorrect parameters')
    else:
        m_interest = args.interest / (12 * 100)
        if args.type == 'diff':
            print_differentiated_payments(args.principal, args.periods, m_interest)
        if args.type == 'annuity':
            if args.periods is None:
                print_count_of_periods(args.principal, args.payment, m_interest)
            if args.payment is None:
                print_annuity_payment(args.principal, args.periods, m_interest)
            if args.principal is None:
                print_credit_principal(args.payment, args.periods, m_interest)


if __name__ == '__main__':
    main()
