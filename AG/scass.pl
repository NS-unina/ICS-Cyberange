/* Attack goal */
attackGoal(canSpoof(controlAction4)).
attackGoal(canSpoof(controlAction8)).

attackGoal(lossVisibility(feedbackAction8)).

/* Attacker location */
attackerLocated(vulnHost).
hacl(_,_,_,_).
hacl(X,Y,_,_):-
	inSubnet(X,S),
	inSubnet(Y,S).

/* Control Logic */
/* Control flow Master-PLC to S-PLC*/
controlFlow(mainPLC, genPLC, controlAction4).
feedbackFlow(genPLC, mainPLC, feedbackAction4).
protocol(controlAction4, plaintext).
/* Control flow Scada-System to Master-PLC*/
controlFlow(genPLC, gIED2, controlAction8).
feedbackFlow(gIED2, genPLC, feedbackAction8).
protocol(feedbackAction8, plaintext).
protocol(feedbackAction8, unauthenticated).

inSubnet(mainPLC, scassNet).
l2Discovery(mainPLC, arp).
inSubnet(genPLC, scassNet).
l2Discovery(genPLC, arp).
inSubnet(gIED1, scassNet).
l2Discovery(gIED1, arp).
inSubnet(gIED2, scassNet).
l2Discovery(gIED2, arp).
inSubnet(vulnHost, scassNet).

/* Vulnerabilities */
vulProperty(cve_1999_0667, remoteExploit, privEscalation).
cvss(cve2016_7406,h).
vulProperty(cve2016_7407,remoteExploit, privEscalation).
cvss(cve2016_7407,h).
vulProperty(cve2016_7408,remoteExploit, privEscalation).
cvss(cve2016_7408,h).
vulProperty(cve2016_7409,remoteExploit, informationDisclosure).
cvss(cve2016_7409,l).
vulProperty(cwe_306,remoteExploit, privEscalation).
cvss(cwe_306,h).
vulProperty(cwe_521,remoteExploit, privEscalation).
cvss(cwe_521,h).
vulProperty(cve2017_0267,remoteExploit, informationDisclosure).
cvss(cve2017_0267,m).
vulProperty(cve2017_0268,remoteExploit, informationDisclosure).
cvss(cve2017_0268,m).
vulProperty(cve2017_0269,remoteExploit, denialOfService).
cvss(cve2017_0269,m).
vulProperty(cve2017_0144,remoteExploit, privEscalation).
cvss(cve2017_0144,h).
vulProperty(cve2022_30697, localExploit, privEscalation).
cvss(cve2022_30697,m).
vulProperty(cve2022_26485, remoteClient, privEscalation).
cvss(cve2022_26485,h).
vulProperty(cve2014_6271, remoteClient, privEscalation).
cvss(cve2014_6271,h).
vulProperty(cve2012_0668, remoteClient, privEscalation).
cvss(cve2014_6271,h).
/* End Vulns */