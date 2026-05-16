import json



get = """[GET] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

put = """[PUT] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

post = """[POST] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

patch = """[PATCH] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

delete = """[DELETE] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""


home = """[HOME] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

stats = """[STATS] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

saved = """[SAVED] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""


explore = """[EXPLORE] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

following = """[FOLLOWING] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

featured = """[FEATURED] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""


write = """[WRITE] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

login = """[LOGIN] Sustainability is about making choices that protect our
        planet and ensure resources are available for future generations. 
        By embracing sustainable living, we reduce waste, conserve energy,
        and support eco-friendly products. Simple actions like recycling,
        using reusable items, and choosing local, organic foods can make a big difference. 
        Sustainability also encourages mindful consumption, promoting quality over quantity
        and fostering a deeper connection with nature. Adopting these habits not only benefits 
        the environment but also enhances 
        our well-being and builds a more resilient, responsible lifestyle."""

FUNC_MAP = {'GET': get,
            'POST': post,
            'PUT': put,
            'PATCH': patch,
            'DELETE': delete,
            'HOME': home,
            'STATS': stats,
            'SAVED': saved,
            'EXPLORE': explore,
            'FOLLOWING': following,
            'FEATURED': featured,
            'WRITE': write,
            'LOGIN': login,
            }

def lambda_handler(event, context):
    print(f"event : {event}")
    access_control_request_method = event['headers'].get('access-control-request-method', '')
    method = event['requestContext']['http']['method']
    if access_control_request_method and method == 'OPTIONS':
        response = FUNC_MAP[access_control_request_method]
    else:
        response = FUNC_MAP[method]
    return {
        'statusCode': 200,
        'body': json.dumps(f"""Hello from {method} endpoint! 
        Here's some info about sustainability:
        {response}""")
}





if __name__ == "__main__":
    test_event = {
        "headers": {
            'access-control-request-method': 'LOGIN'
        },
        "requestContext": {
            "http": {
                "path": "/login",
                "method": "LOGIN"
            }
        }
    }
    response = lambda_handler(test_event, None)
    print(response)