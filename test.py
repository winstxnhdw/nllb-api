from asyncio import TaskGroup

from httpx import AsyncClient
from uvloop import run

text = 'Once upon a time in a quiet little village nestled between rolling hills, there lived a young girl named Lila. Lila had always been curious about the world beyond the village. Every evening, she would sit by her window, gazing at the stars, wondering what adventures awaited her beyond the horizon.\n\nOne day, while exploring the forest near her home, Lila stumbled upon an ancient oak tree. The tree was larger than any other in the forest, its trunk wide and covered in moss. As Lila circled the tree, she noticed something strange—a small, shimmering key was embedded in the bark.\n\n"What could this unlock?" Lila wondered, her heart racing with excitement. With great care, she pulled the key from the tree. The moment she did, the ground beneath her began to tremble. A hidden door at the base of the oak creaked open, revealing a spiral staircase descending deep into the earth.\n\nCuriosity overwhelmed her, and Lila carefully made her way down the staircase. At the bottom, she discovered a vast underground cavern filled with glowing crystals. In the center of the cavern stood a pedestal, and atop it lay a dusty old book.\n\nThe book\'s cover was worn, its pages yellowed with age, but it seemed to hum with a strange energy. Lila cautiously opened the book, and to her amazement, the pages were filled with stories—stories about magical lands, brave heroes, and terrible monsters. But the most astonishing thing of all was that Lila\'s name appeared in every one of them.\n\n"How is this possible?" Lila whispered. She turned page after page, reading about adventures she had yet to experience, battles she would one day fight, and friends she had not yet met. The book told her of a great quest that awaited her—a journey to find the lost city of Aurelia, where an ancient power was said to be hidden.\n\nLila felt a strange pull in her heart. The world she had always dreamed of exploring was calling her, and now she knew that her destiny lay beyond the village. She tucked the book under her arm, her mind racing with thoughts of the journey ahead.\n\nAs she left the cavern and ascended the staircase, Lila knew that her life would never be the same. The world was vast and full of wonders, and she was ready to discover them all. With the key in her pocket and the book in her hands, Lila stepped out into the sunlight, determined to begin her adventure.\n\nAnd so, with courage in her heart and a sparkle of excitement in her eyes, Lila set off towards the horizon, ready to write her own story.'


async def test_server_async():
    """
    Summary
    -------
    test the server asynchronously
    """
    async with AsyncClient(base_url='https://winstxnhdw-nllb-api.hf.space/api/v4', timeout=None) as client:
        async with TaskGroup() as task:
            _ = [
                task.create_task(
                    client.post('/translator', json={'text': text, 'source': 'eng_Latn', 'target': 'spa_Latn'})
                )
                for _ in range(4)
            ]


def test_server():
    """
    Summary
    -------
    test the server
    """
    run(test_server_async())


if __name__ == '__main__':
    test_server()
