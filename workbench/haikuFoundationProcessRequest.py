import json


post = ("[POST] Sustainability is about making choices that protect our "
        "planet and ensure resources are available for future generations."
        "By embracing sustainable living, we reduce waste, conserve energy,"
        "and support eco-friendly products. Simple actions like recycling,"
        "using reusable items, and choosing local, organic foods can make a big difference. "
        "Sustainability also encourages mindful consumption, promoting quality over quantity"
        "and fostering a deeper connection with nature. Adopting these habits not only benefits "
        "the environment but also enhances our well-being and builds a more resilient, responsible lifestyle.")

get = ("[GET] Sustainability is about making choices that protect our "
        "planet and ensure resources are available for future generations."
        "By embracing sustainable living, we reduce waste, conserve energy,"
        "and support eco-friendly products. Simple actions like recycling,"
        "using reusable items, and choosing local, organic foods can make a big difference. "
        "Sustainability also encourages mindful consumption, promoting quality over quantity"
        "and fostering a deeper connection with nature. Adopting these habits not only benefits "
        "the environment but also enhances our well-being and builds a more resilient, responsible lifestyle.")

put = ("[put] Sustainability is about making choices that protect our "
        "planet and ensure resources are available for future generations."
        "By embracing sustainable living, we reduce waste, conserve energy,"
        "and support eco-friendly products. Simple actions like recycling,"
        "using reusable items, and choosing local, organic foods can make a big difference. "
        "Sustainability also encourages mindful consumption, promoting quality over quantity"
        "and fostering a deeper connection with nature. Adopting these habits not only benefits "
        "the environment but also enhances our well-being and builds a more resilient, responsible lifestyle.")

patch = ("[patch] Sustainability is about making choices that protect our "
        "planet and ensure resources are available for future generations."
        "By embracing sustainable living, we reduce waste, conserve energy,"
        "and support eco-friendly products. Simple actions like recycling,"
        "using reusable items, and choosing local, organic foods can make a big difference. "
        "Sustainability also encourages mindful consumption, promoting quality over quantity"
        "and fostering a deeper connection with nature. Adopting these habits not only benefits "
        "the environment but also enhances our well-being and builds a more resilient, responsible lifestyle.")

delete = ("[delete] Sustainability is about making choices that protect our "
        "planet and ensure resources are available for future generations."
        "By embracing sustainable living, we reduce waste, conserve energy,"
        "and support eco-friendly products. Simple actions like recycling,"
        "using reusable items, and choosing local, organic foods can make a big difference. "
        "Sustainability also encourages mindful consumption, promoting quality over quantity"
        "and fostering a deeper connection with nature. Adopting these habits not only benefits "
        "the environment but also enhances our well-being and builds a more resilient, responsible lifestyle.")


head = ("[head] Sustainability is about making choices that protect our "
        "planet and ensure resources are available for future generations."
        "By embracing sustainable living, we reduce waste, conserve energy,"
        "and support eco-friendly products. Simple actions like recycling,"
        "using reusable items, and choosing local, organic foods can make a big difference. "
        "Sustainability also encourages mindful consumption, promoting quality over quantity"
        "and fostering a deeper connection with nature. Adopting these habits not only benefits "
        "the environment but also enhances our well-being and builds a more resilient, responsible lifestyle.")

options = ("[options] Sustainability is about making choices that protect our "
        "planet and ensure resources are available for future generations."
        "By embracing sustainable living, we reduce waste, conserve energy,"
        "and support eco-friendly products. Simple actions like recycling,"
        "using reusable items, and choosing local, organic foods can make a big difference. "
        "Sustainability also encourages mindful consumption, promoting quality over quantity"
        "and fostering a deeper connection with nature. Adopting these habits not only benefits "
        "the environment but also enhances our well-being and builds a more resilient, responsible lifestyle.")


requestPathLookup = {
    "/home": "Home Controller",
    "/following": "Following Controller",
    "/explore": "Explore Controller",
    "/featured": "Featured Controller",
    "/write": "Assistant Controller",
    "/stats": "Stats Controller",
    "/saved": "Saved Controller",
    "/login": "Login Controller",
    "/signup": "Signup Controller",
}

httpMethodLookup = {'GET': get,
            'POST': post,
            'PUT': put,
            'PATCH': patch,
            'DELETE': delete,
            'HEAD': head,
            'OPTIONS': options
            }

def lambda_handler(event, context):
    print(f"event : {event}")
    httpMethod = event.get('httpMethod')
    resp = httpMethodLookup[httpMethod]
    final_response = {
        'statusCode': 200,
        'body': json.dumps(resp)
    }
    return final_response

if __name__ == "__main__":
    test_event = {
        "httpMethod": "GET"
    }
    response = lambda_handler(test_event, None)
    print(response)
