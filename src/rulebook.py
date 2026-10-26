from common import *
from game import *
from mascot import kopeikin
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Flowable, PageBreak, NextPageTemplate
from reportlab.lib.styles import ParagraphStyle
body = ParagraphStyle('body', fontName='Mono', fontSize=8.9, leading=11.2, spaceAfter=3.2, textColor=black)
bul = ParagraphStyle('bul', parent=body, leftIndent=11, bulletIndent=1, spaceAfter=2.2); num = ParagraphStyle('num', parent=bul)
gls = ParagraphStyle('gls', parent=body, fontName='MonoI', fontSize=8.1, leading=10, textColor=FLAV, spaceAfter=4)
glo = ParagraphStyle('glo', parent=body, fontSize=8.0, leading=9.8, spaceAfter=2.6, leftIndent=8, firstLineIndent=-8)
B = lambda s: '<font name="MonoB">%s</font>' % s
class Head(Flowable):
    def __init__(self, text, size=12.5, top=7): Flowable.__init__(self); self.text, self.size, self.top = text, size, top; self.keepWithNext = 1
    def wrap(self, aw, ah): self.aw = aw; return aw, self.size+self.top+7
    def draw(self): c = self.canv; hdraw(c, self.text, 0, 5, 'HeadB', self.size, color=RED, anchor='l'); c.setStrokeColor(black); c.setLineWidth(0.7); c.line(0, 1.5, self.aw, 1.5)
def P(t): return Paragraph(t, body)
def Bl(t): return Paragraph(t, bul, bulletText='\xb7')
def N(i, t): return Paragraph(t, num, bulletText='%d.' % i)
def G(t): return Paragraph(t, gls)
def quota():
    data = [['Players', 'Year 1', 'Year 2', 'Year 3', 'Year 4']] + [[k] + [fmt(v) for v in vals] for k, vals in QUOTAS.items()]
    t = Table(data, colWidths=[62, 46, 46, 46, 46], rowHeights=13)
    t.setStyle(TableStyle([('FONT', (0, 0), (-1, 0), 'MonoB', 8.2), ('FONT', (0, 1), (-1, -1), 'Mono', 8.4), ('FONT', (0, 1), (0, -1), 'MonoB', 8.4), ('BACKGROUND', (0, 0), (-1, 0), black), ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('GRID', (0, 0), (-1, -1), 0.5, black), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    t.hAlign = 'LEFT'; return t
K = fmt(KULAK)
S = [Head('The game in one minute', top=0),
  P('MONOPOLITBURO is Monopoly under Stalin. Nobody owns anything: you pay the State to be appointed %s of an enterprise, and you charge %s to comrades who land on it. One player is the %s, who runs the bank, collects every tax and fine, and must pay Moscow a rising quota each Year. Everyone else is a %s, getting rich while trying not to look rich.' % (B('Director'), B('fees'), B('Party Secretary'), B('citizen'))),
  P('The game lasts four Years, about 90 to 120 minutes. Nobody is ever eliminated. They are merely replaced.'),
  G('The subtitle is a real slogan: the first Five-Year Plan (1928-32) was declared complete a year early.'),
  Head('What you need'),
  Bl('The Monopoly board with its stickers applied, and all of its money except the 1s and 5s. Amounts are called rubles, and every amount in the game is a multiple of 10.'),
  Bl('28 deeds, 16 Directives from Moscow, 16 Kitchen Rumors, 12 character cards, 1 Secretary aid, 5 citizen aids, 6 Suspicion trackers, 15 Blat chits.'),
  Bl('About 10 black glass beads: one per citizen for Suspicion, one for the Year track.'),
  Bl('Dice and tokens. The Secretary takes a token too. Add a third die for 6 players.'),
  Bl('%s as Workshops and %s as Kombinats. Return the other 12 houses and 4 hotels to the box.' % (B('20 houses'), B('8 hotels'))),
  G('Kombinat: a large integrated industrial complex.'),
  Head('1. Roles'), Bl('One player is the Party Secretary, chosen by volunteering or by the highest roll. Everyone else is a citizen.'), Bl('The Secretary runs the bank, holds the District Fund, directs no enterprises and pays no fees.'),
  Head('2. Setup'), Bl('Each citizen gets 1,500 rubles, one random character card, a Suspicion tracker and 2 random deeds dealt free. With 6 players, deal 3.'),
  Bl('Every citizen starts at Suspicion 0. The Poet starts at 2.'), Bl("The Secretary's District Fund starts at 200 rubles and sits face up on the Year track for all to see."),
  Bl('The building supply is 20 Workshops and 8 Kombinats. It is never replenished.'), Bl('Put a bead on Year 1 of the Year track.'),
  Head("3. A citizen's turn"), Bl('Roll two dice and move. Doubles roll again. Three doubles in a row send you to the Gulag for being suspiciously lucky.'), Bl('Collect 200 rubles whenever you land on or pass Poluchka.'),
  Bl('%s pay the bank its price %s to be appointed Director. If you decline, the Secretary auctions it at once.' % (B('Unowned enterprise:'), B('plus 20 per point of your Suspicion'))),
  Bl('%s pay its Director the fee on the deed. A Director in the Gulag collects nothing.' % B('Directed enterprise:')),
  Bl('A full colour group doubles the base fee and allows building, as in the original. Build evenly. A Kombinat costs the Workshop price plus four Workshops returned to supply.'),
  Bl('%s take the pledge value on the deed from the bank, collect no fees on it, and redeem it for the redeem value printed beside it.' % B('Pledging an enterprise to the State:')),
  Bl('%s instead of buying or building this turn, pay 100 to the District Fund to drop 1 Suspicion.' % B('Subbotnik:')),
  Bl('%s once per round, on your own turn, pay the Secretary 50 to give another citizen +1 Suspicion. You cannot target anyone in the Gulag. If it puts them at 5, you drop 1.' % B('Denounce:')),
  Bl('%s you may skip your next turn to take 1 Blat. Landing on the Gulag corner as a visitor drops 1 Suspicion.' % B('Ochered:')),
  Bl('%s if two citizens want the last buildings, the Secretary decides who gets them. Gifts are welcome.' % B('Shortage:')),
  Bl('Citizens may trade freely with each other at any time. A deal with the Secretary binds only if it is paid on the spot.'),
  G('Ochered: the queue. Blat: the informal economy of favors that got you what rubles could not. Subbotnik: a day of "voluntary" unpaid Saturday labor.'),
  Head('4. Auctions'), Bl('The Secretary opens the bidding at 10. Anyone may bid, and bids rise in 10s. The Secretary never bids.'),
  Bl('The winner pays at once, adding 20 per point of their own Suspicion. The Secretary keeps 30 in the District Fund and the rest goes to the bank.'),
  Head("5. The Secretary's turn"), Bl('The Secretary goes last each round. Roll two dice and move, with no doubles bonus. With 6 players, roll three dice and keep the best two.'),
  Bl('%s on a directed enterprise, the Director pays a bribe equal to the current fee. The amount is negotiable. A Director who refuses gains +2 Suspicion.' % B('Inspection:')),
  Bl('On an unowned enterprise, the Secretary auctions it immediately.'), Bl('On The Midnight Knock, the Secretary chooses one citizen to gain +1 Suspicion.'),
  Bl('Once per round, on their own turn, the Secretary may denounce one citizen at no cost.'),
  Bl('The Secretary cannot be sent to the Gulag and never collects at Poluchka. All taxes, fines, card payments, Gulag fees, denunciation fees, surcharges, auction cuts and forged-paper fees go to the District Fund.'),
  P(B('What the Secretary may bend:') + ' any bribe amount; the price of pardons, release, Blat and forged papers; which enterprise reverts when a citizen is disappeared; who gets the last buildings; anything the rules do not cover.'),
  P(B('What the Secretary may not bend:') + ' fees, prices, quotas or card effects; refusing to hold an auction; taking from the bank; hiding the District Fund.'),
  Head('6. Years and quotas'), P('A Year ends when the Secretary lands on or passes Poluchka. Resolve these steps in order:'),
  N(1, 'The richest citizen by net worth gains +2 Suspicion and the second richest +1. Tied citizens all gain it.'), N(2, "The Secretary pays Moscow's quota from the District Fund to the bank."),
  N(3, 'A Secretary who cannot pay is purged (section 9).'), N(4, 'After the Year 4 quota is resolved, the game ends.'), Spacer(1, 3), quota(), Spacer(1, 5),
  G('Kulak: a "wealthy" peasant, which in practice meant anyone with two cows and an enemy.'),
  Head('7. Suspicion'), P('Each citizen has a Suspicion tracker from 0 to 5, marked with a bead in plain view.'),
  Bl('%s denunciation +1, refusing an Inspection bribe +2, richest at year end +2 and second +1, The Midnight Knock +1, some cards.' % B('It rises:')),
  Bl('%s Subbotnik, forged papers, a successful denunciation, visiting the Gulag, Doska Pochyota and Socialist Emulation.' % B('It falls:')),
  Bl('%s hold up to 3. Spend one to cancel a single payment of up to 200 rubles, or to block 1 Suspicion as you gain it.' % B('Blat:')),
  Bl('%s on your turn, pay the Secretary 150 rubles (negotiable) to draw a new character and drop 2 Suspicion.' % B('Forged papers:')),
  P(B('At 5 you are disappeared:')), N(1, 'Go to the Gulag.'), N(2, 'The Secretary picks one of your enterprises to revert to the State. Buildings in that colour group are sold back at half price, and you keep the proceeds.'),
  N(3, 'If you direct no enterprises, pay the Secretary 100 rubles, or all your cash if you have less.'), N(4, 'Your character goes face down on the Unpersons pile. "They were never here. Check the photograph."'),
  N(5, 'Draw a new character and reset Suspicion to 0. The Red Army Officer, if in play, gains +1.'),
  P('If the character deck runs out, shuffle the Unpersons pile to form a new deck. They have been rehabilitated.'), G("Rehabilitation: the official clearing of a purge victim's name, usually posthumous."),
  Head('8. The Gulag'), Bl('To leave, roll doubles, pay 50 rubles, play a release card or make a deal with the Secretary. You move with the roll that frees you.'), Bl('After 3 failed turns you must pay 50 and move.'),
  Bl('While inside, you collect no fees.'), G('Gulag: acronym for the Main Administration of Camps, which ran the Soviet forced-labor camp system.'),
  Head('9. Purges and bankruptcy'), P(B('A purged Secretary:')), Bl('The citizen with the lowest Suspicion becomes Secretary. Ties go to the richest. Skip the Former Person. One does not decline.'),
  Bl("The new Secretary's enterprises revert to the State unpledged, their cash becomes the District Fund, and their character goes to the Unpersons pile."),
  Bl('The old Secretary draws a character, receives 500 rubles from the bank and starts at Suspicion 3.'),
  Bl('If the Secretary misses the Year 4 quota, there is no replacement. The State has failed, and the richest citizen wins whatever their net worth.'),
  P(B('A bankrupt citizen:')), Bl('Your remaining cash goes to your creditor, and your enterprises revert to the State.'), Bl('Draw a new character, take a 500 ruble stipend, reset Suspicion to 0 and restart from Poluchka.'),
  Head('10. Character timing'), Bl("Bonuses printed on a character (the Former Person's 300 rubles, the Old Bolshevik's and Officer's Blat) are collected whenever you take that card."),
  Bl('Whenever you become the Poet, set your Suspicion to at least 2.'), Bl('For the Old Bolshevik, double the Suspicion gain first, then apply any Blat. Suspicion losses are never doubled.'),
  Bl("The Red Director's discount cannot take a building below 30 rubles."), Bl("The Poet's unchosen card goes to the bottom of its deck."),
  Bl('The Seksot may denounce twice per round. Anyone may denounce the Spekulant for free.'), Bl('Sabotage cards are tagged in the top corner. Each one gives the Spets +1 Suspicion, whoever draws it.'),
  Head('11. Winning'), Bl('%s is your cash, plus the price of each enterprise you direct (pledge value if pledged), plus what you paid for your buildings.' % B('Net worth')),
  Bl('If any citizen ends above the %s, the richest citizen wins.' % B('Kulak Line of %s rubles' % K)), Bl('If nobody does, the sitting Secretary wins, having kept the district properly equal.'),
  Head('12. The golden rule'), P('Where the rules are silent, the Secretary decides. The Secretary may be persuaded.'),
]
GLOSS = [('Anekdot', 'A political joke. Telling one could earn a sentence under Article 58.'), ('Apparatchik', 'A full-time functionary of the Party machine, the "apparat."'), ('Article 58', 'The criminal code article covering "counter-revolutionary activity," defined very loosely.'),
 ('Belomorkanal', 'The White Sea-Baltic Canal, dug by prisoner labor from 1931 to 1933.'), ('Blat', "The informal economy of favors and connections that got you what rubles couldn't."), ('Bolshoi', '"Big." Moscow\'s grand theatre, also used for Party congresses.'),
 ('Brak', 'Defective output, the chronic result of plans that counted quantity only.'), ('Bumazhka', 'A scrap of official paper. "Without a bumazhka you\'re a bug."'), ('Byvshiye lyudi', '"Former people": ex-nobles, merchants and clergy stripped of rights after the Revolution.'),
 ('Dacha', 'A country house.'), ('DniproHES', 'The Dnieper Hydroelectric Station, completed in 1932.'), ('Donos', 'A written denunciation.'), ('Doska pochyota', 'The Board of Honor, displaying portraits of model workers.'),
 ('Dostat', '"To obtain." The verb for getting scarce goods, since simply buying them wasn\'t possible.'), ('Furazhka', "The peaked military cap with a stiff visor. Comrade Kopeikin's hat."), ('Glavlit', 'The central censorship office, founded in 1922.'),
 ('Gosplan', 'The State Planning Committee, which wrote the Five-Year Plans.'), ('Gosstrakh', 'The state insurance monopoly, founded in 1921.'), ('Gulag', 'Acronym for the Main Administration of Camps, which ran the forced-labor camp system.'),
 ('Iz-pod prilavka', '"From under the counter," where shop clerks kept the real inventory.'), ('Kassa', "The cashier's window where wages were paid."), ('Kolkhoz', 'A collective farm. A kolkhoznik is one of its peasants.'), ('Komandirovka', 'An official business trip.'),
 ('Kombinat', 'A large integrated industrial complex.'), ('Kommunalka', 'A communal apartment, with one room per family and a shared kitchen and bathroom.'), ('Kopeika', 'The smallest Soviet coin, one hundredth of a ruble, and the root of Comrade Kopeikin\'s name.'),
 ('Kreml', '"Fortress." The origin of the word Kremlin.'), ('Kulak', 'A "wealthy" peasant, a label applied very freely during collectivization.'), ('MTS', 'Machine-Tractor Station, a state depot that rented machinery to collective farms.'),
 ('Narkomat', "A People's Commissariat, the Soviet name for a ministry until 1946."), ('NKVD', "The People's Commissariat for Internal Affairs, the secret police of the Stalin era."), ('Ochered', 'The queue.'), ('Organs, the', 'Everyday shorthand for the organs of state security.'),
 ('Osoaviakhim', 'A mass "voluntary" civil-defense society.'), ('Partbilet', 'The Party membership card.'), ('Patronymic', "A middle name built from the father's first name, used with the first name as polite address."), ('Poluchka', 'Slang for payday.'),
 ('Pravda', '"Truth." The Party\'s official newspaper.'), ('Premiya', 'The bonus paid for hitting plan targets.'), ('Pripiski', '"Write-ins": the routine inflating of plan results.'), ('Prodavets', 'A shop clerk.'), ('Propiska', 'The residence permit stamped in the internal passport.'),
 ('Putyovka', 'A trade-union voucher for a state holiday resort.'), ('Rehabilitation', "The official clearing of a purge victim's name, usually posthumous."), ('Seksot', 'Short for "secret collaborator," an informant for the secret police.'), ('Shabashka', 'An off-the-books side job.'),
 ('Shturmovshchina', '"Storming": the frantic month-end scramble to meet the plan.'), ('Socialist emulation', 'Official competition between work brigades for banners and pennants.'), ('Spekulant', 'A black marketeer. Reselling goods for profit was a crime.'),
 ('Spets', 'A "bourgeois specialist" trained before the Revolution.'), ('Stakhanovite', 'A record-setting worker, named for miner Alexei Stakhanov.'), ('Stolovaya', 'A workplace canteen.'), ('Subbotnik', 'A day of "voluntary" unpaid Saturday labor.'),
 ('Tolkuchka', 'A "push market," a tolerated flea market.'), ('Torgsin', 'State shops (1931-36) that sold scarce goods only for gold, silver or foreign currency.'), ('Turksib', 'The Turkestan-Siberia Railway, finished in 1931.'),
 ('Udarnik', 'A "shock worker," the official title for quota-smashers.'), ('VEB', 'Volkseigener Betrieb, "people-owned enterprise," the prefix of every East German state firm.'), ('Voronok', '"Little raven," the nickname for the black police vans.'), ('Vreditelstvo', '"Wrecking": the charge of deliberate industrial sabotage.')]
S += [Head('Glossary'), G('Every Russian word and Soviet term in the game.')] + [Paragraph('%s  %s' % (B(t), m), glo) for t, m in GLOSS]
S += [Head('Change log'), G('MONOPOLITBURO is in beta. Every printed piece carries its version. Rules changes bump the middle number, wording and layout fixes the last.'),
  P(B('v0.2.0, October 2026.') + ' After two playtests.'),
  Bl('Denunciation is once per round, not once per Year. The Seksot gets two. The Secretary gets one free.'), Bl('Refusing an Inspection bribe is +2 Suspicion. The richest citizen takes +2 at year end and the second richest +1.'),
  Bl('Appointments and auction wins cost 20 extra per point of the buyer\'s Suspicion.'), Bl('New ways down: Subbotnik (100 to drop 1), a denunciation that jails someone (drop 1), visiting the Gulag corner (drop 1).'),
  Bl('Auctions spelled out: opens at 10, bids in 10s, Secretary keeps 30.'), Bl('The Secretary\'s powers and limits written down. The District Fund is public.'),
  Bl('Quotas raised. Kulak Line lowered from 4,000 to %s. A Secretary who misses the final quota hands the win to the richest citizen.' % K),
  Bl('Red Army Officer: free railways and 1 Blat, but +1 Suspicion whenever anyone is disappeared. The Year 3 penalty is gone.'),
  Bl('All amounts rounded to 10s and the 1 and 5 notes retired. Pledge and redeem values printed on every deed, with the purchase price.'),
  Bl('Aids are single-sided. Suspicion trackers are separate cards, the Year track is a board sticker, and black glass beads replace the house and hotel markers.'),
  P(B('v0.1.0, September 2026.') + ' First printed set.')]
S += [Head('Building your copy'), P(B('Board stickers, in this order:')),
  N(1, 'The four corners and the 14 full-space stickers. Each carries its own black border and sits over the board\'s printed lines.'), N(2, 'The 22 name patches, tucked against the colour bar.'), N(3, 'The two deck labels, over the Chance and Community Chest outlines.'),
  N(4, 'The title bar, piece A then piece B.'), N(5, 'The mascot piece last.'), N(6, 'The maker\'s mark over the oval logo, and the Year track below the title bar.'),
  P(B('Cards:')), Bl('Directives on orange stock and Kitchen Rumors on yellow, one side only.'), Bl('Deeds and character cards are double-sided: print a FRONTS page, flip the sheet on its long edge, then print the BACKS page that follows it.'),
  Bl('Aids and trackers are single-sided on ivory stock. Chits on white.'),
  P(B('Tuning:') + ' the quota track, the Kulak Line and the 200 ruble starting Fund are still estimates. If the Secretary is purged every game, lower the quotas. If the Secretary always wins, lower the Kulak Line. Only the two aids, the Year sticker and this rulebook carry those numbers.')]

def cover(c, doc):
    c.saveState(); bw = 6.9*IN; bh = bw*0.2; bx = (W-bw)/2; by = H-4.35*IN
    c.saveState(); cp = c.beginPath(); cp.rect(bx, by+bh-2, bw, 4*IN); c.clipPath(cp, stroke=0, fill=0); kopeikin(c, W/2, by+bh-112, 2.5, 'salute'); c.restoreState()
    c.setFillColor(black); c.rect(bx+4, by-4, bw, bh, fill=1, stroke=0); c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(1.4); c.rect(bx, by, bw, bh, fill=1, stroke=1); c.setFillColor(RED); c.rect(bx+6, by+6, bw-12, bh-12, fill=1, stroke=0)
    size = 70
    while sw('MONOPOLITBURO', 'HeadB', size) > bw*0.76: size -= 0.5
    ty = by+bh/2-size*0.35; hdraw(c, 'MONOPOLITBURO', W/2+2.4, ty-2.4, 'HeadB', size, color=black, ucyr=True); hdraw(c, 'MONOPOLITBURO', W/2, ty, 'HeadB', size, color=white, ucyr=True)
    hammer_sickle(c, bx+bw*0.056, by+bh/2, bh*0.21, color=GOLDC); hammer_sickle(c, bx+bw*0.944, by+bh/2, bh*0.21, color=GOLDC)
    c.setFillColor(black); c.setFont('MonoB', 17); c.drawCentredString(W/2, by-34, 'FIVE-YEAR PLAN IN FOUR YEARS!'); hdraw(c, 'Rules of Play', W/2, by-92, 'HeadB', 26, color=RED)
    c.setFillColor(black); c.setFont('Mono', 11.5)
    for i, ln in enumerate(['A game of appointments, quotas and suspicion', 'for 3 to 6 comrades.  90 to 120 minutes.', '', 'One of you is the Party Secretary.', 'The rest of you are citizens, for now.']): c.drawCentredString(W/2, by-128-i*16, ln)
    c.setFillColor(RED); c.setFont('MonoB', 10); c.drawCentredString(W/2, by-224, 'BETA  ' + VERSION)
    ddr_logo(c, W/2, 1.35*IN, True); c.setFillColor(FLAV); c.setFont('MonoI', 8); c.drawCentredString(W/2, 0.62*IN, 'A satire. The jokes are aimed at the system. The history in the grey type is real.'); c.restoreState()
def back(c, doc):
    c.saveState(); kopeikin(c, W/2, H/2-40, 3.0, 'suitcase'); hdraw(c, 'The Plan is complete', W/2, H/2-110, 'HeadB', 24, color=RED)
    c.setFillColor(black); c.setFont('MonoB', 12); c.drawCentredString(W/2, H/2-136, 'If you enjoyed this game, tell no one.'); c.setFillColor(FLAV); c.setFont('MonoI', 9); c.drawCentredString(W/2, H/2-156, 'Comrade Kopeikin keeps a bag packed. He finds it saves time.')
    ddr_logo(c, W/2, 1.35*IN, True); vstamp(c, W-40, 30, size=7); c.restoreState()
def page(c, doc):
    c.saveState(); c.setFillColor(RED); c.rect(40, H-46, W-80, 3, fill=1, stroke=0); hdraw(c, 'MONOPOLITBURO', 40, H-38, 'HeadB', 9, color=black, anchor='l', ucyr=True)
    c.setFillColor(FLAV); c.setFont('Mono', 8); c.drawRightString(W-40, H-38, 'Rules of Play  ' + VERSION); c.drawCentredString(W/2, 28, '- %d -' % doc.page); c.restoreState()
def build(path):
    doc = BaseDocTemplate(path, pagesize=letter, title='MONOPOLITBURO %s - Rules of Play' % VERSION, author='MONOPOLITBURO')
    fw = (W-80-22)/2; fh = H-46-14-48
    frames = [Frame(40, 48, fw, fh, id='l', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0), Frame(40+fw+22, 48, fw, fh, id='r', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)]
    doc.addPageTemplates([PageTemplate(id='cover', frames=[Frame(40, 40, W-80, 20, id='c')], onPage=cover), PageTemplate(id='body', frames=frames, onPage=page), PageTemplate(id='back', frames=[Frame(40, 40, W-80, 20, id='b')], onPage=back)])
    doc.build([NextPageTemplate('body'), PageBreak()] + S + [NextPageTemplate('back'), PageBreak(), Spacer(1, 1)])
if __name__ == '__main__':
    build('../out/Monopolitburo_v0.2.0_5_Rulebook.pdf'); print('ok')
