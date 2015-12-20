from requests import get, post
import urllib2
from bs4 import BeautifulSoup
import random
import telegram
from telegram import Updater

def start(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text='''Hello!\n\n/news - Shows top 6 news on bbc
                  /weather - Weather forecast for 3 days
                  /funny - Bruce faces''')

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def talking(bot, update):
    msg = update.message.text
    msg = ''.join(random.sample(msg,len(msg)))
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def news(bot, update):
    news_page = 'http://www.bbc.com/news'
    news_page_code = get(news_page)
    news_page_soup = BeautifulSoup(news_page_code.content.decode(news_page_code.encoding), "lxml")
    top_news = []
    counter = 0
    for span in news_page_soup.findAll('span', attrs={'class': 'title-link__title-text'}):
        counter += 1
        top_news.append(str(counter) + ". " + u''.join(map(unicode, span.contents)))
        if counter == 6:
            break
    top_news = u'\n'.join(top_news)
    bot.sendMessage(chat_id=update.message.chat_id, text="Top news:\n"+top_news+"\n\nMore at " + news_page)

def weather(bot, update):
    weather_page = 'http://www.weather-forecast.com/locations/Moscow/forecasts/latest#forecast-part-0'
    weather_code = get(weather_page)
    weather_soup = BeautifulSoup(weather_code.content.decode(weather_code.encoding), "lxml")
    weather_description_for_three_days = []
    time_list = []
    max_temperature = []
    min_temperature = []
    counter = 9
    
    for span in weather_soup.findAll('div', attrs={'class' : 'pname'}):
        if counter == 0:
            break
        if u''.join(span.contents) == u"AM":
            time_list.append(u"Morning:")
        elif u''.join(span.contents) == u"PM":
            time_list.append(u"Afternoon:")
        else:
            time_list.append(u"Night:")
        counter -= 1
    if time_list[0] == u"Morning:":
        const_counter = 9
    elif time_list[0] == u"Afternoon:":
        const_counter = 8
    elif time_list[0] == u"Night:":
        const_counter = 7
    counter = const_counter
    for span in weather_soup.findAll('td', attrs={'class' : 'med wphrase', 'align' : 'center'}):
        text = u''.join(span.findAll('div')[0].findAll('b')[0].contents)
        weather_description_for_three_days.append(text)
        if counter == 0:
            break
        counter -= 1
    counter = const_counter
    for span in weather_soup.findAll('span', attrs={'class' : 'temp'}):
        max_temperature.append(u''.join(span.contents) + u"\u00B0 C")
        if counter == 1:
            break
        counter -= 1
    counter = const_counter + 9
    for span in weather_soup.findAll('span', attrs={'class' : 'temp'}):
        if counter <= const_counter:
            min_temperature.append(u''.join(span.contents) + u"\u00B0 C")
        if counter == 1:
            break
        counter -= 1
    
    weather_forecast = []
    for index in xrange(0, const_counter):
        if index == 0:
            weather_forecast.append(u"Today:")
        elif index == const_counter - 6:
            weather_forecast.append(u"Tomorrow:")
        elif index == const_counter - 3:
            weather_forecast.append(u"Day after:")
        weather_forecast.append(u" " + time_list[index] + u" " +
                                weather_description_for_three_days[index] + u" min: "
                                + min_temperature[index] + u" max: " + max_temperature[index])
    weather_forecast = u"\n".join(weather_forecast)
    bot.sendMessage(chat_id=update.message.chat_id, text=weather_forecast)

def funny(bot, update):
    imges = []
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr06/21/15/grid-cell-16959-1393013724-14.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr06/21/15/grid-cell-14782-1393013713-4.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr06/21/15/grid-cell-14785-1393013692-7.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr07/21/15/grid-cell-13653-1393013679-2.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr04/21/15/grid-cell-13708-1393013642-3.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr03/21/15/grid-cell-32297-1393013776-5.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr06/21/15/grid-cell-16670-1393013862-7.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr03/21/15/grid-cell-843-1393013874-12.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr03/21/15/grid-cell-574-1393013898-5.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr06/21/15/grid-cell-16892-1393013910-14.jpg')
    imges.append('http://ak-hdl.buzzfed.com/static/2014-02/enhanced/webdr06/21/15/grid-cell-16572-1393013948-12.jpg')
    bot.sendPhoto(chat_id=update.message.chat_id, photo=imges[random.randint(0, len(imges) - 1)])

def main():
    my_bot_token = "117933540:AAFN18Xs583FQpTyYQjogw6IMHKgsyVGpPw"
    updater = Updater(token=my_bot_token)
    dispatcher = updater.dispatcher
    
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramMessageHandler(talking)
    dispatcher.addUnknownTelegramCommandHandler(unknown)
    dispatcher.addTelegramCommandHandler('news', news)
    dispatcher.addTelegramCommandHandler('weather', weather)
    dispatcher.addTelegramCommandHandler('funny', funny)
    updater.start_polling()

if __name__ == "__main__":
    main()
