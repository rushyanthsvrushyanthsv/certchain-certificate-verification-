import hashlib
import json
from datetime import datetime


class Blockchain:

    def __init__(self):
        self.chain = []

        # Genesis block
        self.create_block(
            producer="SYSTEM",
            consumer="SYSTEM",
            energy=0,
            price=0,
            transaction_id="GENESIS"
        )

    def calculate_hash(self, index, timestamp, data, previous_hash):
        block_string = (
            str(index)
            + str(timestamp)
            + json.dumps(data, sort_keys=True)
            + str(previous_hash)
        )

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()

    def create_block(
        self,
        producer,
        consumer,
        energy,
        price,
        transaction_id
    ):

        index = len(self.chain)

        timestamp = datetime.now().isoformat()

        data = {
            "producer": producer,
            "consumer": consumer,
            "energy_kwh": energy,
            "price_per_kwh": price,
            "transaction_id": transaction_id
        }

        previous_hash = (
            self.chain[-1]["hash"]
            if self.chain
            else "0"
        )

        block_hash = self.calculate_hash(
            index,
            timestamp,
            data,
            previous_hash
        )

        block = {
            "index": index,
            "timestamp": timestamp,
            "data": data,
            "previous_hash": previous_hash,
            "hash": block_hash
        }

        self.chain.append(block)

        return block

    def verify_chain(self):

        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i - 1]

            calculated_hash = self.calculate_hash(
                current["index"],
                current["timestamp"],
                current["data"],
                current["previous_hash"]
            )

            if current["hash"] != calculated_hash:
                return False

            if current["previous_hash"] != previous["hash"]:
                return False

        return True