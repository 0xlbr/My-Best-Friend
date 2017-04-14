def say_whether_you_liked_the_movie(title):
    ps = {'t': title, 'r': "json", 'tomatoes' : True}
    response = requests.get('http://www.omdbapi.com/?',params = ps)
    rating = int(response.json() ["Ratings"] [1] ["Value"] [:-1])
    if rating >= 70:
        return build_response({}, build_speechlet_response("Author", "<speak>" + "Yes, it was really good!" +  "</speak>", "Yes, I liked it", "I'm still here", False))
    else:
        return build_response({}, build_speechlet_response("Author", "<speak>" + "No, it was not for me." +  "</speak>", "No, I did not like it", "I'm still here", False))
