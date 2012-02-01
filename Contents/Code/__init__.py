from datetime import datetime, timedelta
import math, re

####################################################################################################

TITLE                         = "BBC iPlayer"

BBC_URL                       = "http://www.bbc.co.uk"
BBC_FEED_URL                  = "http://feeds.bbc.co.uk"
BBC_SD_PLAYER_URL             = "%s/iplayer/episode/%%%%s#%%s" % BBC_URL
BBC_HD_PLAYER_URL             = "%s/iplayer/episode/%%s/hd" % BBC_URL
BBC_LIVE_TV_URL               = "%s/iplayer/tv/%%s/watchlive#%%s" % BBC_URL
BBC_LIVE_RADIO_URL            = "%s/iplayer/radio/%%s/listenlive" % BBC_URL
BBC_SD_THUMB_URL              = "http://node2.bbcimg.co.uk/iplayer/images/episode/%s_640_360.jpg"
BBC_HD_THUMB_URL              = "http://node2.bbcimg.co.uk/iplayer/images/episode/%s_832_468.jpg"
BBC_RADIO_CHANNEL_THUMB_URL   = "%s/iplayer/img/radio/%%s.gif" % BBC_URL
BBC_TV_CHANNEL_THUMB_URL      = "%s/iplayer/img/tv/%%s.jpg" % BBC_URL

BBC_SEARCH_URL                = "%s/iplayer/search?q=%%s&page=%%s" % BBC_URL
BBC_SEARCH_TV_URL             = BBC_SEARCH_URL + "&filter=tv"
BBC_SEARCH_RADIO_URL          = BBC_SEARCH_URL + "&filter=radio"

ART_DEFAULT                   = "art-default.jpg"
ART_WALL                      = "art-wall.jpg"
ICON_DEFAULT                  = "icon-default.png"
ICON_SEARCH                   = "icon-search.png"
ICON_PREFS                    = "icon-prefs.png"

####################################################################################################

def Start():

  Plugin.AddPrefixHandler("/video/iplayer", MainMenu, TITLE, ICON_DEFAULT, ART_WALL)
  Plugin.AddViewGroup("Menu", viewMode = "List", mediaType = "items")
  Plugin.AddViewGroup("Info", viewMode = "InfoList", mediaType = "items")
  MediaContainer.art = R(ART_DEFAULT)
  MediaContainer.viewGroup = "Menu"
  MediaContainer.title1 = TITLE
  DirectoryItem.thumb = R(ICON_DEFAULT)
  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-agent'] = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11"

####################################################################################################

def MainMenu():
  dir = MediaContainer()

  dir.Append(Function(DirectoryItem(RSSListContainer, title = "TV Highlights"), url = BBC_FEED_URL + "/iplayer/highlights/tv"))
  dir.Append(Function(DirectoryItem(RSSListContainer, title = "Radio Highlights"), url = BBC_FEED_URL + "/iplayer/highlights/radio"))

  dir.Append(Function(DirectoryItem(RSSListContainer, title = "Most Popular TV"), url = BBC_FEED_URL + "/iplayer/popular/tv"))
  dir.Append(Function(DirectoryItem(RSSListContainer, title = "Most Popular Radio"), url = BBC_FEED_URL + "/iplayer/popular/radio"))

  dir.Append(Function(DirectoryItem(AddTVChannels, title = "TV Channels")))
  dir.Append(Function(DirectoryItem(AddRadioStations, title = "Radio Stations")))

  dir.Append(Function(DirectoryItem(AddCategories, title = "Categories")))
  dir.Append(Function(DirectoryItem(AddFormats, title = "Formats")))

  dir.Append(Function(DirectoryItem(AddAToZ, title = "A to Z")))

  dir.Append(Function(InputDirectoryItem(Search, title="Search TV", prompt="Search for TV Programmes", thumb=R(ICON_SEARCH)), search_url = BBC_SEARCH_TV_URL))
  dir.Append(Function(InputDirectoryItem(Search, title="Search Radio", prompt="Search for Radio Programmes", thumb=R(ICON_SEARCH)), search_url = BBC_SEARCH_RADIO_URL))

  dir.Append(PrefsItem(title="Preferences", thumb=R(ICON_PREFS)))

  return dir

####################################################################################################

def AddTVChannels(sender, query = None):

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC One", subtitle = sender.itemTitle, summary = L("summary-bbc_one"), thumb = BBC_TV_CHANNEL_THUMB_URL % "bbc_one"), type = "tv", rss_channel_id = "bbc_one", json_channel_id = "bbcone", json_region_id = "london", live_id = "bbc_one_london"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Two", subtitle = sender.itemTitle, summary = L("summary-bbc_two"), thumb = BBC_TV_CHANNEL_THUMB_URL % "bbc_two"), type = "tv", rss_channel_id = "bbc_two", json_channel_id = "bbctwo", json_region_id = "england", live_id = "bbc_two_england"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Three", subtitle = sender.itemTitle, summary = L("summary-bbc_three"), thumb = BBC_TV_CHANNEL_THUMB_URL % "bbc_three"), type = "tv", rss_channel_id = "bbc_three", json_channel_id = "bbcthree", live_id = "bbc_three"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Four", subtitle = sender.itemTitle, summary = L("summary-bbc_four"), thumb = BBC_TV_CHANNEL_THUMB_URL % "bbc_four"), type = "tv", rss_channel_id = "bbc_four", json_channel_id = "bbcfour", live_id = "bbc_four"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "CBBC", subtitle = sender.itemTitle, summary = L("summary-cbbc"), thumb = BBC_TV_CHANNEL_THUMB_URL % "cbbc"), type = "tv", rss_channel_id = "cbbc", json_channel_id = "cbbc", live_id = "cbbc"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "CBeebies", subtitle = sender.itemTitle, summary = L("summary-cbeebies"), thumb = BBC_TV_CHANNEL_THUMB_URL % "cbeebies_1"), type = "tv", rss_channel_id = "cbeebies", thumb_id = "cbeebies_1", json_channel_id = "cbeebies", live_id = "cbeebies"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC News Channel", subtitle = sender.itemTitle, summary = L("summary-bbc_news24"), thumb = BBC_TV_CHANNEL_THUMB_URL % "bbc_news24"), type = "tv", rss_channel_id = "bbc_news24", json_channel_id = "bbcnews", live_id = "bbc_news24"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Parliament", subtitle = sender.itemTitle, summary = L("summary-bbc_parliament"), thumb = BBC_TV_CHANNEL_THUMB_URL % "bbc_parliament_1"), type = "tv", rss_channel_id = "bbc_parliament", thumb_id = "bbc_parliament_1", json_channel_id = "parliament", live_id = "bbc_parliament"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC HD", subtitle = sender.itemTitle, thumb = BBC_TV_CHANNEL_THUMB_URL % "bbc_hd_1"), type = "tv", rss_channel_id = "bbc_hd", thumb_id = "bbc_hd_1", json_channel_id = "bbchd", thumb_url = BBC_HD_THUMB_URL, player_url = BBC_HD_PLAYER_URL))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Alba", subtitle = sender.itemTitle, thumb = BBC_TV_CHANNEL_THUMB_URL % "bbc_alba"), type = "tv", rss_channel_id = "bbc_alba", json_channel_id = "bbcalba", live_id = "bbc_alba"))

  return dir

####################################################################################################

def AddRadioStations(sender, query = None):

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Radio 1", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_radio_one"), type = "radio", rss_channel_id = "bbc_radio_one", json_channel_id = "radio1", json_region_id = "england", live_id = "bbc_radio_one"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC 1Xtra", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_1xtra"), type = "radio", rss_channel_id = "bbc_1xtra", json_channel_id = "1xtra", live_id = "bbc_1xtra"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Radio 2", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_radio_two"), type = "radio", rss_channel_id = "bbc_radio_two", json_channel_id = "radio2", live_id = "bbc_radio_two"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Radio 3", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_radio_three"), type = "radio", rss_channel_id = "bbc_radio_three", json_channel_id = "radio3", live_id = "bbc_radio_three"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Radio 4 FM", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_radio_four"), type = "radio", rss_channel_id = "bbc_radio_four", json_channel_id = "radio4", json_region_id = "fm", live_id = "bbc_radio_fourfm"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Radio 4 LW", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_radio_four"), type = "radio", rss_channel_id = "bbc_radio_four", json_channel_id = "radio4", json_region_id = "lw", live_id = "bbc_radio_fourlw"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Radio 4 Extra", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_radio_four"), type = "radio", rss_channel_id = "bbc_radio_four_extra", thumb_id = "bbc_radio_four", json_channel_id = "radio4extra", live_id = "bbc_radio_four_extra"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Radio 5 live", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_radio_five_live"), type = "radio", rss_channel_id = "bbc_radio_five_live", json_channel_id = "5live", live_id = "bbc_radio_five_live"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Radio 5 live sports extra", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_radio_five_live_sports_extra"), type = "radio", rss_channel_id = "bbc_radio_five_live_sports_extra", json_channel_id = "5livesportsextra", live_id = "bbc_radio_five_live_sports_extra"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC 6 Music", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_6music"), type = "radio", rss_channel_id = "bbc_6music", json_channel_id = "6music", live_id = "bbc_6music"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC Asian Network", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_asian_network"), type = "radio", rss_channel_id = "bbc_asian_network", json_channel_id = "asiannetwork", live_id = "bbc_asian_network"))
  dir.Append(Function(DirectoryItem(ChannelContainer, title = "BBC World Service", subtitle = sender.itemTitle, thumb = BBC_RADIO_CHANNEL_THUMB_URL % "bbc_world_service"), type = "radio", rss_channel_id = "bbc_world_service", json_channel_id = "worldservice", live_id = "bbc_world_service"))

  return dir

####################################################################################################

def AddCategories(sender, query = None, channel_name = None, channel_id = None, thumb = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  # returns a list of the various categories / genres displayed on the iPlayer web site

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  dir.Append(Function(DirectoryItem(CategoryContainer, title = "Children's", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "childrens", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(CategoryContainer, title = "Comedy", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "comedy", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(CategoryContainer, title = "Drama", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "drama", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(CategoryContainer, title = "Entertainment", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "entertainment", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(CategoryContainer, title = "Factual", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "factual", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(CategoryContainer, title = "Learning", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "learning", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(CategoryContainer, title = "Music", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "music", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(CategoryContainer, title = "News", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "news", channel_id = channel_id, has_subcategories = 0, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(CategoryContainer, title = "Sport", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, category_id = "sport", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))

  return dir

####################################################################################################

def AddFormats(sender, query = None, channel_name = None, channel_id = None, thumb = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  # returns a list of the various programme formats displayed on the iPlayer web site

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  dir.Append(Function(DirectoryItem(FormatContainer, title = "Animation", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "animation", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Appeals", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "appeals", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Bulletins", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "bulletins", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Discussion & Talk", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "discussionandtalk", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Docudramas", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "docudramas", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Documentaries", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "documentaries", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Films", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "films", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Games & Quizzes", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "gamesandquizzes", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Magazines & Reviews", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "magazinesandreviews", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Makeovers", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "makeovers", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Performances & Events", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "performancesandevents", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Phone-ins", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "phoneins", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Readings", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "readings", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Reality", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "reality", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))
  dir.Append(Function(DirectoryItem(FormatContainer, title = "Talent Shows", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, format_id = "talentshows", channel_id = channel_id, thumb_url = thumb_url, player_url = player_url))

  return dir

####################################################################################################

def AddAToZ(sender, query = None):

  # returns an A-Z list of links to an RSS feed for each letter (plus 0-9)

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Menu")

  for letter in range (65, 91):
    thisLetter = chr(letter)
    dir.Append(Function(DirectoryItem(RSSListContainer, title = thisLetter, subtitle = sender.itemTitle), url = BBC_FEED_URL + "/iplayer/atoz/%s/list" % thisLetter, sort_list = "alpha"))

  dir.Append(Function(DirectoryItem(RSSListContainer, title = "0-9", subtitle = sender.itemTitle), url = BBC_FEED_URL + "/iplayer/atoz/0-9/list", sort_list = "alpha"))

  return dir

####################################################################################################

def Search(sender, query, search_url = BBC_SEARCH_URL, page_num = 1):

  dir = None

  searchResults = HTTP.Request(search_url % (String.Quote(query),page_num)).content

  # Extract out JS object which contains program info.
  match = re.search('episodeRegistry\\.addData\\((.*?)\\);',searchResults, re.IGNORECASE | re.DOTALL)

  if match:
    jsonObj = JSON.ObjectFromString(match.group(1))
    if jsonObj:

      eps = jsonObj.values()

      # Try to extract out the order of the show out of the html as the JSON object is a dictionary keyed by PID which means 
      # the results order can't be guaranteed by just iterating through it.    
      epOrder = []
      for  match in re.finditer('class="cta-add-to-favourites" href="pid-(.*?)"',searchResults):
        epOrder.append(match.group(1))

      eps.sort(key=lambda ep: (ep['id'] in epOrder and (epOrder.index(ep['id']) + 1)) or 1000)

      dir = JSONSSearchListContainer(sender,eps)

  if not dir or len(dir) == 0:
    return MessageContainer(header = sender.itemTitle, message = "No programmes found.")
  else:
    if page_num > 1:
      dir.Insert(0,Function(DirectoryItem(Search, title='Previous...', thumb=R(ICON_SEARCH)), query = query, search_url = search_url, page_num = page_num - 1))

    # See if we need a next button.
    if (re.search('title="Next page"', searchResults)):
      dir.Append(Function(DirectoryItem(Search, title='More...', thumb=R(ICON_SEARCH)), query = query, search_url = search_url, page_num = page_num + 1))

  return dir

####################################################################################################

def WeekdayName(inDate):

  # utility function to convert a weekday index into a string

  if inDate.weekday() == 0:
  	return "Monday"
  elif inDate.weekday() == 1:
    return "Tuesday"
  elif inDate.weekday() == 2:
    return "Wednesday"
  elif inDate.weekday() == 3:
    return "Thursday"
  elif inDate.weekday() == 4:
    return "Friday"
  elif inDate.weekday() == 5:
    return "Saturday"
  elif inDate.weekday() == 6:
    return "Sunday"

####################################################################################################

def MonthName(inDate):

  # utility function to convert a month index into a string

  if inDate.month == 1:
  	return "January"
  elif inDate.month == 2:
    return "February"
  elif inDate.month == 3:
    return "March"
  elif inDate.month == 4:
    return "April"
  elif inDate.month == 5:
    return "May"
  elif inDate.month == 6:
    return "June"
  elif inDate.month == 7:
    return "July"
  elif inDate.month == 8:
    return "August"
  elif inDate.month == 9:
    return "September"
  elif inDate.month == 10:
    return "October"
  elif inDate.month == 11:
    return "November"
  elif inDate.month == 12:
    return "December"

####################################################################################################

def ChannelContainer(sender, query = None, type = "None", rss_channel_id = None, json_channel_id = None, json_region_id = None, live_id = None, thumb_id = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  if type == "tv":
    if thumb_id == None:
      thumb = BBC_TV_CHANNEL_THUMB_URL % rss_channel_id
    else:
      thumb = BBC_TV_CHANNEL_THUMB_URL % thumb_id
  else:
    if thumb_id == None:
      thumb = BBC_RADIO_CHANNEL_THUMB_URL % rss_channel_id
    else:
      thumb = BBC_RADIO_CHANNEL_THUMB_URL % thumb_id

  if live_id != None:
    if type == "tv":
      dir.Append(WebVideoItem(url = BBC_LIVE_TV_URL % (live_id, Prefs['sd_video_quality']), title = "On Now", subtitle = sender.itemTitle, thumb = thumb, duration = 0))
    else:
      dir.Append(WebVideoItem(url = BBC_LIVE_RADIO_URL % live_id, title = "On Now", subtitle = sender.itemTitle, thumb = thumb, duration = 0))

  if rss_channel_id != None:
    dir.Append(Function(DirectoryItem(RSSListContainer, title = "Highlights", subtitle = sender.itemTitle, thumb = thumb), url = BBC_FEED_URL + "/iplayer/highlights/" + rss_channel_id, subtitle = sender.itemTitle, thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(RSSListContainer, title = "Most Popular", subtitle = sender.itemTitle, thumb = thumb), url = BBC_FEED_URL + "/iplayer/popular/" + rss_channel_id, subtitle = sender.itemTitle, thumb_url = thumb_url, player_url = player_url))

  if json_channel_id != None:
    if json_region_id != None:
      json_region_id_path = json_region_id + "/"
    else:
      json_region_id_path = ""
    dir.Append(Function(DirectoryItem(AddCategories, title = "Categories", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, channel_id = json_channel_id, thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(JSONScheduleListContainer, title = "Today", subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/%s/programmes/schedules/%stoday.json" % (json_channel_id, json_region_id_path), subtitle = sender.itemTitle, thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(JSONScheduleListContainer, title = "Yesterday", subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/%s/programmes/schedules/%syesterday.json" % (json_channel_id, json_region_id_path), subtitle = sender.itemTitle, thumb_url = thumb_url, player_url = player_url))
    now = datetime.today()
    oneDay = timedelta(days = 1)
    for i in range (2, 7):
      thisDate = now - (i * oneDay)
      dir.Append(Function(DirectoryItem(JSONScheduleListContainer, WeekdayName(thisDate) + " " + str(thisDate.day) + " " + MonthName(thisDate), subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/%s/programmes/schedules/%s%s/%s/%s.json" % (json_channel_id, json_region_id_path, thisDate.year, thisDate.month, thisDate.day), subtitle = sender.itemTitle, thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(AddFormats, title = "Formats", subtitle = sender.itemTitle, thumb = thumb), thumb = thumb, channel_id = json_channel_id, thumb_url = thumb_url, player_url = player_url))

  return dir

####################################################################################################

def CategoryContainer(sender, query = None, channel_id = None, category_id = None, thumb = None, has_subcategories = 1, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  if channel_id == None:

    # global category container, so split the category further by All / TV / Radio

    dir.Append(Function(DirectoryItem(RSSListContainer, title = "TV Highlights", subtitle = sender.itemTitle, thumb = thumb), url = BBC_FEED_URL + "/iplayer/highlights/" + category_id + "/tv", thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(RSSListContainer, title = "Radio Highlights", subtitle = sender.itemTitle, thumb = thumb), url = BBC_FEED_URL + "/iplayer/highlights/" + category_id + "/radio", thumb_url = thumb_url, player_url = player_url))

    dir.Append(Function(DirectoryItem(RSSListContainer, title = "Most Popular TV", subtitle = sender.itemTitle, thumb = thumb), url = BBC_FEED_URL + "/iplayer/popular/" + category_id + "/tv", thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(RSSListContainer, title = "Most Popular Radio", subtitle = sender.itemTitle, thumb = thumb), url = BBC_FEED_URL + "/iplayer/popular/" + category_id + "/radio", thumb_url = thumb_url, player_url = player_url))

    if has_subcategories == 1:
      dir.Append(Function(DirectoryItem(SubCategoryContainer, title = "Sub-categories", subtitle = sender.itemTitle, thumb = thumb), category_id = category_id, thumb = thumb))

    dir.Append(Function(DirectoryItem(JSONEpisodeListContainer, title = "All programmes", subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/programmes/genres/%s/player/episodes.json" % category_id, empty_title = sender.itemTitle, list_type = "category", thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(JSONEpisodeListContainer, title = "TV programmes", subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/tv/programmes/genres/%s/player/episodes.json" % category_id, empty_title = sender.itemTitle, empty_name = "TV", list_type = "category", thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(JSONEpisodeListContainer, title = "Radio programmes", subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/radio/programmes/genres/%s/player/episodes.json" % category_id, empty_title = sender.itemTitle, empty_name = "radio", list_type = "category", thumb_url = thumb_url, player_url = player_url))

  else:

    # channel-specific category container, so return a list of categories for this channel

    return JSONEpisodeListContainer(sender, url = "http://www.bbc.co.uk/%s/programmes/genres/%s/player/episodes.json" % (channel_id, category_id), owning_channel = sender.title1, empty_title = sender.itemTitle, empty_name = sender.title1, list_type = "category", thumb_url = thumb_url, player_url = player_url)

  return dir

####################################################################################################

def SubCategoryContainer(sender, query = None, channel_id = None, category_id = None, thumb = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  if category_id == "childrens":
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Animation", sub_category_id = "animation", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Drama", sub_category_id = "drama", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Entertainment & Comedy", sub_category_id = "entertainment_and_comedy", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Factual", sub_category_id = "factual", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Games & Quizzes", sub_category_id = "games_and_quizzes", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Music", sub_category_id = "music", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Other", sub_category_id = "other", thumb_url = thumb_url, player_url = player_url))

  elif category_id == "comedy":
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Music", sub_category_id = "music", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Satire", sub_category_id = "satire", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Sitcoms", sub_category_id = "sitcoms", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Sketch", sub_category_id = "sketch", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Spoof", sub_category_id = "spoof", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Standup", sub_category_id = "standup", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Other", sub_category_id = "other", thumb_url = thumb_url, player_url = player_url))

  elif category_id == "drama":
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Action & Adventure", sub_category_id = "action_and_adventure", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Biographical", sub_category_id = "biographical", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Classic & Period", sub_category_id = "classic_and_period", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Crime", sub_category_id = "crime", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Historical", sub_category_id = "historical", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Horror & Supernatural", sub_category_id = "horror_and_supernatural", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Legal & Courtroom", sub_category_id = "legal_and_courtroom", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Medical", sub_category_id = "medical", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Musical", sub_category_id = "musical", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Psychological", sub_category_id = "psychological", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Relationships & Romance", sub_category_id = "relationships_and_romance", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "SciFi & Fantasy", sub_category_id = "scifi_and_fantasy", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Soaps", sub_category_id = "soaps", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Thriller", sub_category_id = "thriller", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "War & Disaster", sub_category_id = "war_and_disaster", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Other", sub_category_id = "other", thumb_url = thumb_url, player_url = player_url))

  elif category_id == "entertainment":
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Discussion & Talk Shows", sub_category_id = "discussion_and_talk_shows", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Games & Quizzes", sub_category_id = "games_and_quizzes", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Makeovers", sub_category_id = "makeovers", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Phone-ins", sub_category_id = "phoneins", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Reality", sub_category_id = "reality", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Talent Shows", sub_category_id = "talent_shows", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Variety Shows", sub_category_id = "variety_shows", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Other", sub_category_id = "other", thumb_url = thumb_url, player_url = player_url))

  elif category_id == "factual":
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Antiques", sub_category_id = "antiques", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Arts, Culture & the Media", sub_category_id = "arts_culture_and_the_media", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Beauty & Style", sub_category_id = "beauty_and_style", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Cars & Motors", sub_category_id = "cars_and_motors", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Cinema", sub_category_id = "cinema", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Consumer", sub_category_id = "consumer", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Crime & Justice", sub_category_id = "crime_and_justice", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Disability", sub_category_id = "disability", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Families & Relationships", sub_category_id = "families_and_relationships", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Food & Drink", sub_category_id = "food_and_drink", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Health & Wellbeing", sub_category_id = "health_and_wellbeing", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "History", sub_category_id = "history", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Homes & Gardens", sub_category_id = "homes_and_gardens", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Life Stories", sub_category_id = "life_stories", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Money", sub_category_id = "money", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Pets & Animals", sub_category_id = "pets_and_animals", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Politics", sub_category_id = "politics", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Science & Nature", sub_category_id = "science_and_nature", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Travel", sub_category_id = "travel", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Other", sub_category_id = "other", thumb_url = thumb_url, player_url = player_url))

  elif category_id == "learning":
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Pre-School", sub_category_id = "preschool", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "5-11", sub_category_id = "511", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Adult", sub_category_id = "adult", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Other", sub_category_id = "other", thumb_url = thumb_url, player_url = player_url))

  elif category_id == "music":
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Classic Pop & Rock", sub_category_id = "classic_pop_and_rock", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Classical", sub_category_id = "classical", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Country", sub_category_id = "country", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Dance & Electronica", sub_category_id = "dance_and_electronica", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Desi", sub_category_id = "desi", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Easy Listening, Soundtracks & Musicals", sub_category_id = "easy_listening_soundtracks_and_musicals", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Folk", sub_category_id = "folk", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Hip Hop, R'n'B & Dancehall", sub_category_id = "hip_hop_rnb_and_dancehall", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Jazz & Blues", sub_category_id = "jazz_and_blues", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Pop & Chart", sub_category_id = "pop_and_chart", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Rock & Indie", sub_category_id = "rock_and_indie", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Soul & Reggae", sub_category_id = "soul_and_reggae", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "World", sub_category_id = "world", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Other", sub_category_id = "other", thumb_url = thumb_url, player_url = player_url))

  elif category_id == "sport":
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Boxing", sub_category_id = "boxing", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Cricket", sub_category_id = "cricket", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Cycling", sub_category_id = "cycling", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Equestrian", sub_category_id = "equestrian", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Football", sub_category_id = "football", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Formula One", sub_category_id = "formula_one", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Golf", sub_category_id = "golf", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Horse Racing", sub_category_id = "horse_racing", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Motorsport", sub_category_id = "motorsport", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Olympics", sub_category_id = "olympics", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Rugby League", sub_category_id = "rugby_league", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Rugby Union", sub_category_id = "rugby_union", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Tennis", sub_category_id = "tennis", thumb_url = thumb_url, player_url = player_url))
    dir.Append(SubCategoryItem(category_name = sender.title2, category_id = category_id, sub_category_name = "Other", sub_category_id = "other", thumb_url = thumb_url, player_url = player_url))

  return dir

####################################################################################################

def SubCategoryItem(category_name = None, category_id = None, sub_category_name = None, sub_category_id = None, thumb = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  return Function(DirectoryItem(RSSListContainer, title = sub_category_name, subtitle = category_name, thumb = thumb), url = BBC_FEED_URL + "/iplayer/categories/" + category_id + "/" + sub_category_id + "/list", sort_list = "alpha", thumb_url = thumb_url)

####################################################################################################

def FormatContainer(sender, query = None, channel_id = None, format_id = None, thumb = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  if channel_id == None:

    # global format container, so split the format further by All / TV / Radio

    dir.Append(Function(DirectoryItem(JSONEpisodeListContainer, title = "All programmes", subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/programmes/formats/%s/player/episodes.json" % format_id, empty_title = sender.itemTitle, list_type = "format", thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(JSONEpisodeListContainer, title = "TV programmes", subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/tv/programmes/formats/%s/player/episodes.json" % format_id, empty_title = sender.itemTitle, empty_name = "TV", list_type = "format", thumb_url = thumb_url, player_url = player_url))
    dir.Append(Function(DirectoryItem(JSONEpisodeListContainer, title = "Radio programmes", subtitle = sender.itemTitle, thumb = thumb), url = "http://www.bbc.co.uk/radio/programmes/formats/%s/player/episodes.json" % format_id, empty_title = sender.itemTitle, empty_name = "radio", list_type = "format", thumb_url = thumb_url, player_url = player_url))

  else:

    # channel-specific format container, so return a list of formats for this channel

    return JSONEpisodeListContainer(sender, url = "http://www.bbc.co.uk/%s/programmes/formats/%s/player/episodes.json" % (channel_id, format_id), owning_channel = sender.title1, empty_title = sender.itemTitle, empty_name = sender.title1, list_type = "format", thumb_url = thumb_url, player_url = player_url)

  return dir

####################################################################################################

def RSSListContainer(sender, query = None, url = None, subtitle = None, sort_list = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  # this function generates the highlights, most popular and sub-category lists from an RSS feed
  
  feed = RSS.FeedFromString(url)
  if feed is None: return

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  for entry in feed.entries:

    # the URL chunk to use as the program's UID is different for HD programs
    # default to using the 2nd-to-last chunk
    thumb = thumb_url % entry["link"].split("/")[-3]
    if thumb_url == BBC_HD_THUMB_URL:
      # ...unless it's an HD URL, in which case use the 3rd-to-last chunk
      thumb = thumb_url % entry["link"].split("/")[-4]

    parts = entry["title"].split(": ")

    if len(parts) == 3:
      title = "%s: %s" % (parts[0], parts[2])
    else:
      title = entry["title"]
      
    if subtitle == None:
      # find out if this is a tv or radio show
      thisSubtitle = "TV"
      for category in entry.categories:
        if category[1] == "Radio":
          thisSubtitle = "Radio"
    else:
      thisSubtitle = subtitle

    content = HTML.ElementFromString(entry["content"][0].value)
    summary = content.xpath("p")[1].text.strip()
    
     # Only append quality setting if non-HD stream otherwise HD site config won't get picked.
    thisUrl = entry["link"]
    if (player_url != BBC_HD_PLAYER_URL):
      thisUrl += "#" + Prefs['sd_video_quality']
		
    dir.Append(WebVideoItem(url = thisUrl, title = title, subtitle = thisSubtitle, summary = summary, duration = 0, thumb = thumb))
    
  if sort_list == "alpha":
    dir.Sort("title")

  if len(dir) == 0:
    return MessageContainer(header = sender.itemTitle, message = "No programmes found.")

  return dir

####################################################################################################

def JSONEpisodeListContainer(sender, query = None, url = None, owning_channel = None, empty_title = None, empty_name = None, list_type = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  # this function generates the category lists and format lists from a JSON feed

  jsonObj = JSON.ObjectFromURL(url)
  if jsonObj is None: return

  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  episodes = jsonObj["episodes"]
  
  for programme in episodes:
  
    thisProgramme = programme["programme"]
    displayTitles = thisProgramme["display_titles"]
    title = displayTitles["title"]
    foundSubtitle = displayTitles["subtitle"]
    pid = thisProgramme["pid"]
    short_synopsis = thisProgramme["short_synopsis"]

    # find out the owning channel for this content, if none was provided
    
    thisOwningChannel = owning_channel
    if thisOwningChannel == None:

      if thisProgramme.has_key("programme"):
        thisSubProgramme = thisProgramme["programme"]

        if thisSubProgramme.has_key("ownership"):
          thisOwnership = thisSubProgramme["ownership"]
          if thisOwnership.has_key("service"):
            thisService = thisOwnership["service"]
            thisOwningChannel = thisService["title"]

        elif thisSubProgramme.has_key("programme"):
          thisSubSubProgramme = thisSubProgramme["programme"]
          if thisSubSubProgramme.has_key("ownership"):
            thisOwnership = thisSubSubProgramme["ownership"]
            if thisOwnership.has_key("service"):
              thisService = thisOwnership["service"]
              thisOwningChannel = thisService["title"]

    # check we now have an owning channel, and substitute the channel type if not

    if thisOwningChannel == None:
      if empty_name == "TV":
        thisOwningChannel = "TV"
      elif empty_name == "radio":
        thisOwningChannel = "Radio"

    if foundSubtitle != "":
      dir.Append(WebVideoItem(url = player_url % pid, title = "%s - %s" % (title, foundSubtitle), subtitle = thisOwningChannel, summary = short_synopsis, duration = 0, thumb = thumb_url % pid))
    else:
      dir.Append(WebVideoItem(url = player_url % pid, title = title, subtitle = thisOwningChannel, summary = short_synopsis, duration = 0, thumb = thumb_url % pid))
  
  # sort the programmes alphabetically by title (we always do this for categories and for formats)
  dir.Sort("title")
  
  if len(dir) == 0:
    if empty_name != None:
      return MessageContainer(header = empty_title, message = "No %s programmes found for this %s." % (empty_name, list_type))
    else:
      return MessageContainer(header = empty_title, message = "No programmes found for this %s." % list_type)

  return dir

####################################################################################################

def JSONScheduleListContainer(sender, query = None, url = None, subtitle = None, thumb_url = BBC_SD_THUMB_URL, player_url = BBC_SD_PLAYER_URL % Prefs['sd_video_quality']):

  # this function generates the schedule lists for today / yesterday etc. from a JSON feed

  jsonObj = JSON.ObjectFromURL(url)
  if jsonObj is None: return
  
  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  day = jsonObj["schedule"]["day"]
  
  for broadcast in day["broadcasts"]:

    start = broadcast["start"][11:16]
    duration = broadcast["duration"] * 1000 # in milliseconds
    thisProgramme = broadcast["programme"]
    displayTitles = thisProgramme["display_titles"]
    title = displayTitles["title"]
    foundSubtitle = displayTitles["subtitle"]
    pid = thisProgramme["pid"]
    short_synopsis = thisProgramme["short_synopsis"] + "\n\n" + "Duration: " + DurationAsString(duration)
    
    # assume unavailable unless we can find an expiry date of after now
    available = 0
    nowDate = 0
    expiryDate = 0
    if thisProgramme.has_key("media"):
      media = thisProgramme["media"]
      if media.has_key("expires"):
        available = 1
        nowDate = datetime.utcnow()
        if media["expires"] == None:
          # use an expiry date in the distant future
          expiryDate = nowDate + timedelta(days = 1000)
        else:
          expiryDate = BBCDateToUTCPythonDate(media["expires"])

    if available == 1 and expiryDate > nowDate:
      if foundSubtitle != "":
        dir.Append(WebVideoItem(url = player_url % pid, title = "%s %s" % (start, title), subtitle = foundSubtitle, summary = short_synopsis, duration = duration, thumb = thumb_url % pid))
      else:
        dir.Append(WebVideoItem(url = player_url % pid, title = "%s %s" % (start, title), subtitle = subtitle, summary = short_synopsis, duration = duration, thumb = thumb_url % pid))
    else:
      if foundSubtitle != "":
        dir.Append(Function(DirectoryItem(NotAvailableOniPlayerContainer, title = "%s %s" % (start, title), subtitle = foundSubtitle, summary = short_synopsis + "\n\nNot currently available on iPlayer.", thumb = thumb_url % pid), header = "%s - %s" % (title, foundSubtitle), message = "This programme is not currently available on iPlayer."))
      else:
        dir.Append(Function(DirectoryItem(NotAvailableOniPlayerContainer, title = "%s %s" % (start, title), subtitle = subtitle, summary = short_synopsis + "\n\nNot currently available on iPlayer.", thumb = thumb_url % pid), header = title, message = "This programme is not currently available on iPlayer."))
  
  return dir

####################################################################################################

def JSONSSearchListContainer(sender, jsonObj = None, thumb_url = BBC_SD_THUMB_URL):

  # this function generates the schedule lists for today / yesterday etc. from a JSON feed
  if jsonObj is None: return
  
  dir = MediaContainer(title1 = sender.title2, title2 = sender.itemTitle, viewGroup = "Info")

  for progInfo in jsonObj:

    url = BBC_URL + progInfo['my_url'] + "#" + Prefs['sd_video_quality']
    duration = int(progInfo['duration']) * 1000
    title = progInfo['complete_title']
    foundSubtitle = progInfo['masterbrand_title']
    broadcast_date = BBCDateToUTCPythonDate(progInfo['original_broadcast_datetime']).strftime('%a, %d. %b %Y %I:%M%p')
    pid = progInfo['id']
    short_synopsis = progInfo['short_synopsis'] + "\n\nBroadcast On: " +  broadcast_date + "\nDuration: " + DurationAsString(duration)
    
    if progInfo.has_key("availability") and progInfo["availability"] == 'CURRENT':
      dir.Append(WebVideoItem(url = url, title = title, subtitle = foundSubtitle, summary = short_synopsis, duration = duration, thumb = thumb_url % pid))
    else:
      dir.Append(Function(DirectoryItem(NotAvailableOniPlayerContainer, title = title, subtitle = foundSubtitle, summary = short_synopsis + "\n\nNot currently available on iPlayer.", thumb = thumb_url % pid), header = "%s - %s" % (title, foundSubtitle), message = "This programme is not currently available on iPlayer."))
  
  return dir

####################################################################################################

def NotAvailableOniPlayerContainer(sender, query = None, header = None, message = None):

  return MessageContainer(header = header, message = message)

####################################################################################################

def DurationAsString(duration):

  # a utility function to convert a duration in microseconds into a string of hours and minutes

  microsecondsInAMinute = 1000 * 60
  microsecondsInAnHour = microsecondsInAMinute * 60
  hours = int(math.floor(duration / microsecondsInAnHour))
  minutes = int(math.floor((duration - (hours * microsecondsInAnHour)) / microsecondsInAMinute))
  if hours == 0 and minutes == 1:
    return str(minutes) + " minute"
  elif hours == 0 and minutes > 0:
    return str(minutes) + " minutes"
  elif hours == 1 and minutes == 0:
    return str(hours) + " hour"
  elif hours == 1 and minutes > 0:
    return str(hours) + " hour " + str(minutes) + " minutes"
  elif hours > 1 and minutes == 0:
    return str(hours) + " hours"
  else:
    return str(hours) + " hours " + str(minutes) + " minutes"

####################################################################################################

def BBCDateToUTCPythonDate(bbcDate):

  # a utility function to convert a BBC JSON date / time e.g. 2009-09-29T03:55:00+01:00 into a python datetime in UTC

  localPythonDate = datetime.strptime(bbcDate[0:19], "%Y-%m-%dT%H:%M:%S")

  if bbcDate[19] == "Z":
    # already in UTC, so no timezone modification needed
    return localPythonDate
  else:
    timezoneDelta = timedelta(hours = int(bbcDate[20:22]), minutes = int(bbcDate[23:25]))
    if bbcDate[19] == "-":
      utcPythonDate = localPythonDate + timezoneDelta
    else:
      utcPythonDate = localPythonDate - timezoneDelta

  return utcPythonDate