import base58


class Util:
    """Internal Utility Class"""

    @staticmethod
    def validate_wallet(input_wallet: str) -> str:
        if ".sol" in input_wallet:
            return [False, "sd", input_wallet]
        else:
            if base58.b58decode_check(input_wallet):
                return[True, "w", input_wallet]
            else:
                raise Exception("Invalid (non-base58/non-SNS-domain) address format provided.")