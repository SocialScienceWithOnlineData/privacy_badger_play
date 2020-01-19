"""
privacy_badger_play provides helper functions for exploring .json exports from the EFF's Privacy Badger browser extension. What is bigger, the number of sites you watch or the number of sites watching you?
"""

import json
import pprint

def sort_dict( adict, decreasing=True ):
  """
  Takes a dictionary and returns a different kind of collection 
  that is ordered on the dictionaries values.
  """
  return( sorted( list(adict.items() ), key=lambda kv: kv[1], reverse=decreasing) )

def isUpper( string ):
  return( string == string.upper() )

def buildTrackerSites( pb_data ):
  tracker_counts = {} # this will store the number of visited sites that each tracker is following you over
  tracker_sites = []
  for tracker_site, visited_sites in pb_data['snitch_map'].items(): #tracker_site is the tracker while tracked_sites is the list of visited sites it is tracking.
    if len(visited_sites) >= 3:
      tracker_site = tracker_site.upper()
    tracker_counts[ tracker_site ] = len(visited_sites)  # the number of visited sites being watched.
  tracker_counts = sort_dict( tracker_counts ) # rearrange this collection so the most egregious trackers are on top.
  tracker_sites = [ site for site, count in tracker_counts ]
  trackers_invasive = [ site for site, count in tracker_counts if site == site.upper() ]
  trackers_benign =  [ site for site, count in tracker_counts if site == site.lower() ]
  #print(tracker_sites)
  #print(trackers_invasive)
  #print(trackers_benign)
  return( tracker_sites, trackers_invasive, trackers_benign )

def buildVisitedSites( pb_data, tracker_sites ):
  # build dictionary of visited sites and the tracker sites following them
  visited_connections = {}
  for tracker_site, tracked_sites in pb_data['snitch_map'].items():
    # go through the snitch map and turn it inside out, turning each 
    #  visited site into a key whose value is the list of its tracker sites.
    for visited_site in tracked_sites:
      # initialize a visited site with an empty list the first time we see it.  
      #   we'll grow this list with tracker sites that are tracking it.
      if visited_site not in visited_connections:
          visited_connections[ visited_site ] = []
      # build list of a visited site's trackers
      visited_connections[ visited_site ].append( tracker_site )
          
  visited_counts = {}
  for visited_site, subscribed_trackers in visited_connections.items():
    for tracker in subscribed_trackers:
      if tracker.upper() in tracker_sites:
        visited_site = visited_site.upper()
    visited_counts[ visited_site ] = len(subscribed_trackers) 
  visited_counts = sort_dict( visited_counts )
  visited_sites = [ site for site, count in visited_counts ]
  visited_invaded = [ site for site, count in visited_counts if site == site.upper() ]
  visited_benign =  [ site for site, count in visited_counts if site == site.lower() ]
  #print( visited_sites )
  #print( visited_invaded )
  #print( visited_benign )
  return( visited_sites, visited_invaded, visited_benign )

def prepPrivacyBadgerData( pb_data ):
  tracker_sites, trackers_invasive, trackers_benign = buildTrackerSites( pb_data )
  visited_sites, visited_invaded, visited_benign = buildVisitedSites( pb_data, tracker_sites )
  return( visited_sites, tracker_sites )
