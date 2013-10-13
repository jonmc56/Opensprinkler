============================================
OpenSprinkler Pi (OSPi) 
Controller based on Google Calendar 
Jon McDermott

This code inspired by and patterned by the demo 
code from http://rayshobby.net
============================================
I've taken the Opensprinkler Google calendar python demo and split it into two pieces. The first piece queries my sprinkler calendar for 'today', and gets all the schedules for today. It writes the schedules to an XML file on the Pi. The second piece will read the schedule XML file periodically, and control the valves. My thinking is that I can schedule the first piece to run just once daily (just after midnight) to get schedules, rather than hitting the calendar all day (and dealing with potential network issues). I will schedule the second piece to run more frequently because it isn't using the network, just reading the local XML file.

I've also changed the code to use Google's 'magic cookie' to access the calendar, so that I don't have to make it public.

Part 1 is done (get_schedule.py), a sample XML output is below. 
Part 2 is in progress (read_schedule.py), it isn't working yet.
Only problem I can think of is that you can't add a new schedule for today 'on the fly', unless you schedule part1 code to run more often. I figure I'll have a separate interface for manual control of stations anyway, so am not concerned about this.

Sample XML for today's schedules:
<SCHEDULES source="get_schedule.py" updated="2013-04-30 22:23:17">
  <purpose>Daily schedule for OpenSprinkler</purpose>
  <schedule_date>2013-04-30</schedule_date>
  <schedule_count>4</schedule_count>
  <zones>
    <zone>
      <name>zone20</name>
      <start>2013-04-30T00:30:00.000-07:00</start>
      <stop>2013-04-30T01:30:00.000-07:00</stop>
    </zone>
    <zone>
      <name>zone19</name>
      <start>2013-04-30T12:30:00.000-07:00</start>
      <stop>2013-04-30T13:30:00.000-07:00</stop>
    </zone>
    <zone>
      <name>zone16</name>
      <start>2013-04-30T16:00:00.000-07:00</start>
      <stop>2013-04-30T17:00:00.000-07:00</stop>
    </zone>
    <zone>
      <name>zone12</name>
      <start>2013-04-30T08:00:00.000-07:00</start>
      <stop>2013-04-30T09:00:00.000-07:00</stop>
    </zone>
  </zones>
</SCHEDULES>
