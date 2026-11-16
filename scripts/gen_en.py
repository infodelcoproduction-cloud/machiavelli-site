# -*- coding: utf-8 -*-
"""Génère en.html (version anglaise du site public) à partir de index.html.

À relancer après chaque modification de index.html :  python3 scripts/gen_en.py
Le script signale tout texte français qu'il n'a plus retrouvé (texte modifié côté FR → traduction à mettre à jour).
"""
import re, sys, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
DST = os.path.join(ROOT, 'en.html')

# ---------- textes de la page (nœuds texte, hors scripts et styles) ----------
T = {
 # en-tête, menu, accueil
 'Menu': 'Menu',
 'Notre stock': 'Our stock',
 'Qui sommes-nous': 'About us',
 'Nos services': 'Our services',
 'Contact': 'Contact',
 'Bienvenue chez Machiavelli': 'Welcome to Machiavelli',
 'Entrez dans le mouvement': 'Step into the movement',
 'Voir notre stock': 'View our stock',
 'Découvrir Machiavelli': 'Discover Machiavelli',
 'LA MAISON': 'THE HOUSE',
 'Qui sommes-': 'About ',
 'nous ?': 'us.',
 'Disponibilité': 'Availability',
 "Toutes nos pièces sont disponibles immédiatement, sans liste d'attente.": 'All our pieces are available immediately, with no waiting list.',
 'Authenticité': 'Authenticity',
 'Chaque montre achetée et vendue est authentifiée par un expert.': 'Every watch we buy and sell is authenticated by an expert.',
 'Garantie': 'Warranty',
 'Garantie d’un an sur tous nos modèles, extensible à 2 ans.': 'One-year warranty on all our models, extendable to 2 years.',
 'Transparence': 'Transparency',
 'Chaque modèle est montré sous tous ses angles, son état est précisé.': 'Every model is shown from every angle, and its condition is clearly stated.',
 'Le fondateur': 'The founder',
 'Nizar Baeri,': 'Nizar Baeri,',
 "l'œil du marché.": 'an eye on the market.',
 "Fort de plusieurs années d'expérience dans l'achat et la revente de montres de luxe, Nizar Baeri suit de près les tendances du marché pour conseiller chaque client, qu'il achète, vende ou cherche une pièce précise.":
   'With several years of experience buying and selling luxury watches, Nizar Baeri follows market trends closely to advise every client, whether they are buying, selling or looking for a specific piece.',
 'Vendre ou acheter,': 'Sell or buy,',
 'en toute confiance.': 'with complete confidence.',
 'Vendre votre montre': 'Sell your watch',
 'Dépôt-vente ou achat immédiat : vous choisissez la formule qui vous convient.': 'Consignment or immediate purchase: you choose the option that suits you.',
 'Proposer ma montre': 'Offer my watch',
 'Acheter votre montre': 'Buy your watch',
 'Choisissez dans notre stock, ou confiez-nous la recherche de la pièce qui vous manque.': 'Choose from our stock, or let us find the piece you are missing.',
 'Voir le stock': 'View the stock',
 'Sourcer ma montre': 'Source my watch',
 'Entretenir votre montre': 'Care for your watch',
 'Révision, polissage et films de protection, posés en collaboration avec Chronoskin.': 'Servicing, polishing and protective films, applied in collaboration with Chronoskin.',
 'Nous contacter': 'Contact us',
 'Nouveautés': 'New arrivals',
 'Dernières': 'Latest',
 'entrées.': 'arrivals.',
 'Voir toutes nos montres': 'View all our watches',
 'Prenez': 'Book an',
 'rendez-vous.': 'appointment.',
 'Nous vous recevons uniquement sur rendez-vous, Rue des Dominicains 15-17 à Liège.': 'We welcome you by appointment only, Rue des Dominicains 15-17 in Liège.',
 'Copier': 'Copy',
 'Rendez-vous': 'Appointments',
 # bandeau légal
 'Mentions légales': 'Legal notice',
 'Conditions générales de vente': 'Terms and conditions of sale',
 'Politique de confidentialité': 'Privacy policy',
 "Machiavelli Watches est un revendeur indépendant de montres d'occasion. Il n'est affilié à aucune maison horlogère ni à aucun distributeur officiel.":
   'Machiavelli Watches is an independent reseller of pre-owned watches. It is not affiliated with any watch brand or any official distributor.',
 # stock
 'Accueil': 'Home',
 'Le stock': 'The stock',
 'Notre': 'Our',
 'stock.': 'stock.',
 'Chercher': 'Search',
 'Trier': 'Sort',
 'Plus récentes': 'Newest',
 'Prix croissant': 'Price, low to high',
 'Prix décroissant': 'Price, high to low',
 'Montres représentées par des illustrations en attendant les photos réelles. Prix TTC en euros (régime de la marge, TVA non récupérable).':
   'Watches shown as illustrations until real photos are available. Prices in euros, VAT included (margin scheme, VAT not recoverable).',
 'Fermer': 'Close',
 # formulaires
 'Vendre': 'Sell',
 'votre montre.': 'your watch.',
 'Décrivez votre pièce : nous revenons vers vous avec une proposition.': 'Describe your piece: we will get back to you with an offer.',
 'Formule souhaitée': 'Preferred option',
 'Dépôt-vente': 'Consignment',
 'Achat immédiat': 'Immediate purchase',
 'Peu importe': 'No preference',
 'Importez ici 3 photos de votre montre, sous différents angles et représentatives de son état.': 'Upload 3 photos of your watch here, from different angles and showing its condition.',
 '3 photos de la montre': '3 photos of the watch',
 'Face': 'Front',
 'Dos': 'Back',
 'Profil': 'Side',
 'Nom de la montre': 'Watch name',
 'Référence': 'Reference',
 'Année': 'Year',
 'État': 'Condition',
 'Full set': 'Full set',
 'Prix désiré (€)': 'Desired price (€)',
 'Votre nom': 'Your name',
 'Téléphone ou e-mail': 'Phone or email',
 'Envoyer ma proposition': 'Send my offer',
 'Sourcer': 'Source',
 'Indiquez la pièce recherchée : nous la cherchons dans notre réseau.': 'Tell us which piece you are looking for: we will search our network.',
 'Référence recherchée': 'Reference wanted',
 '(facultatif)': '(optional)',
 'Prix maximum (€)': 'Maximum price (€)',
 'Téléphone': 'Phone',
 'E-mail': 'Email',
 'Lancer la recherche': 'Start the search',
 'Merci,': 'Thank you,',
 "c'est presque fait.": 'almost done.',
 'Retour au site': 'Back to the website',
 # pages légales
 'Informations légales': 'Legal information',
 'Dernière mise à jour : 14 novembre 2026': 'Last updated: 14 November 2026 · English translation provided for information; the French version prevails.',
 'Mentions': 'Legal',
 'légales.': 'notice.',
 'Éditeur du site': 'Website publisher',
 'Le site machiavelliwatches.com est édité par Machiavelli Trading SRL, société à responsabilité limitée de droit belge, qui exploite la marque Machiavelli Watches.':
   'The machiavelliwatches.com website is published by Machiavelli Trading SRL, a Belgian private limited company, which operates the Machiavelli Watches brand.',
 'Siège social : Place des Combattants 11-13, 6852 Paliseul (Belgique)': 'Registered office: Place des Combattants 11-13, 6852 Paliseul (Belgium)',
 'Boutique, sur rendez-vous : Rue des Dominicains 15-17, 4000 Liège': 'Boutique, by appointment: Rue des Dominicains 15-17, 4000 Liège',
 "Numéro d'entreprise (BCE) : 1021.229.955 · RPM Liège": 'Company number (BCE): 1021.229.955 · RPM Liège',
 'TVA : BE 1021.229.955': 'VAT: BE 1021.229.955',
 'Téléphone et WhatsApp :': 'Phone and WhatsApp:',
 'E-mail :': 'Email:',
 'Responsable de la publication : Nizar Baeri': 'Publication manager: Nizar Baeri',
 'Activité': 'Business',
 "Machiavelli Watches est un commerce de montres de luxe d'occasion : vente, rachat, recherche de pièces sur demande (sourcing), dépôt-vente, ainsi que services d'entretien (révision, polissage, films de protection).":
   'Machiavelli Watches is a pre-owned luxury watch business: sales, buyback, sourcing of pieces on request, consignment, and care services (servicing, polishing, protective films).',
 'Indépendance': 'Independence',
 "Machiavelli Watches est un revendeur indépendant. Il n'est affilié à aucune maison horlogère, à aucune manufacture ni à aucun distributeur officiel, et n'est ni autorisé, ni sponsorisé, ni approuvé par eux. Les noms de marques, de modèles et les références sont cités uniquement pour désigner les pièces proposées ; ils restent la propriété de leurs titulaires respectifs.":
   'Machiavelli Watches is an independent reseller. It is not affiliated with any watch brand, manufacture or official distributor, and is not authorised, sponsored or endorsed by them. Brand names, model names and references are cited solely to identify the pieces offered; they remain the property of their respective owners.',
 "Chaque montre est authentifiée par un expert avant sa mise en vente. Les montres vendues par Machiavelli Watches sont des biens d'occasion : la garantie légale de conformité est limitée à 12 mois à compter de la livraison, durée expressément convenue avec l'acheteur avant la vente et mentionnée sur le bon de commande et la facture. Une extension à 2 ans peut être proposée. Cette garantie est celle de Machiavelli Watches : elle ne constitue pas une garantie du fabricant.":
   'Every watch is authenticated by an expert before it is offered for sale. Watches sold by Machiavelli Watches are second-hand goods: the legal guarantee of conformity is limited to 12 months from delivery, a period expressly agreed with the buyer before the sale and stated on the order form and the invoice. An extension to 2 years may be offered. This warranty is given by Machiavelli Watches and is not a manufacturer\'s warranty.',
 'Prix et ventes': 'Prices and sales',
 "Les prix sont indiqués en euros, toutes taxes comprises. S'agissant de biens d'occasion, ils relèvent du régime particulier d'imposition de la marge bénéficiaire : la TVA n'est pas mentionnée séparément sur la facture et n'est pas récupérable par l'acheteur. Les pièces sont proposées sous réserve de disponibilité ; les informations et photos sont données de bonne foi et peuvent être précisées à tout moment. Le site présente le stock : aucune vente n'y est conclue en ligne. Lorsqu'une vente est conclue à distance avec un consommateur, celui-ci dispose du droit de rétractation de 14 jours prévu par le Code de droit économique, sauf exceptions légales.":
   'Prices are shown in euros, all taxes included. As second-hand goods, they fall under the special margin scheme: VAT is not shown separately on the invoice and cannot be recovered by the buyer. Pieces are offered subject to availability; information and photos are given in good faith and may be clarified at any time. The website presents our stock: no sale is concluded online. When a sale is concluded at a distance with a consumer, the consumer has the 14-day right of withdrawal provided by the Belgian Code of Economic Law, subject to legal exceptions.',
 'Propriété intellectuelle': 'Intellectual property',
 "Les textes, photographies, vidéos, le monogramme MW, l'identité visuelle et la conception du site sont la propriété de Machiavelli Watches ou sont utilisés avec autorisation. Toute reproduction, totale ou partielle, sans accord écrit préalable est interdite.":
   'The texts, photographs, videos, the MW monogram, the visual identity and the design of the website are the property of Machiavelli Watches or are used with permission. Any reproduction, in whole or in part, without prior written consent is prohibited.',
 'Responsabilité et liens': 'Liability and links',
 "Machiavelli Watches veille à l'exactitude des informations publiées, sans pouvoir garantir l'absence d'erreur. Les liens vers WhatsApp, Instagram, TikTok et Facebook mènent vers des services tiers soumis à leurs propres conditions.":
   'Machiavelli Watches takes care to ensure the accuracy of the information published, without being able to guarantee that it is free of errors. Links to WhatsApp, Instagram, TikTok and Facebook lead to third-party services subject to their own terms.',
 'Hébergement': 'Hosting',
 'Le site est hébergé par GitHub Pages, service de GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.':
   'The website is hosted by GitHub Pages, a service of GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, United States.',
 'Droit applicable et litiges': 'Governing law and disputes',
 "Le présent site et son utilisation sont soumis au droit belge. En cas de litige, les tribunaux de Liège sont compétents, sans préjudice des règles impératives protégeant les consommateurs. Un consommateur peut aussi s'adresser gratuitement au Service de médiation pour le consommateur (":
   'This website and its use are governed by Belgian law. In the event of a dispute, the courts of Liège have jurisdiction, without prejudice to the mandatory rules protecting consumers. A consumer may also contact the Consumer Mediation Service free of charge (',
 'Conditions générales': 'Terms and conditions',
 'de vente.': 'of sale.',
 "Les présentes conditions s'appliquent aux ventes, réservations, rachats et dépôts-ventes de montres conclus avec Machiavelli Trading SRL (Machiavelli Watches), Place des Combattants 11-13, 6852 Paliseul, BCE 1021.229.955, boutique sur rendez-vous Rue des Dominicains 15-17, 4000 Liège, +32 484 70 91 09,":
   'These terms apply to sales, reservations, buybacks and consignments of watches concluded with Machiavelli Trading SRL (Machiavelli Watches), Place des Combattants 11-13, 6852 Paliseul, BCE 1021.229.955, boutique by appointment at Rue des Dominicains 15-17, 4000 Liège, +32 484 70 91 09,',
 '. Les dispositions plus favorables que la loi accorde aux consommateurs prévalent toujours.': '. Any more favourable provisions granted to consumers by law always prevail.',
 '1. Les montres': '1. The watches',
 "Toutes les montres proposées sont des montres d'occasion, authentifiées par un expert avant leur mise en vente. Leurs caractéristiques principales (maison, modèle, référence, année, boîte et papiers, état) figurent sur leur fiche. Les photos représentent la pièce vendue ; les traces d'usage propres à une montre d'occasion ne constituent pas un défaut. Les offres sont valables dans la limite des pièces disponibles.":
   'All watches offered are pre-owned watches, authenticated by an expert before being offered for sale. Their main characteristics (brand, model, reference, year, box and papers, condition) are shown on their product page. The photos show the piece being sold; signs of wear typical of a pre-owned watch do not constitute a defect. Offers are valid while pieces remain available.',
 '2. Prix': '2. Prices',
 "Les prix sont indiqués en euros, toutes taxes comprises (TTC). Les montres d'occasion relèvent du régime particulier d'imposition de la marge bénéficiaire : la TVA n'est pas mentionnée séparément sur la facture et n'est pas récupérable par l'acheteur. Les frais de livraison sont en sus et communiqués avant la conclusion de la vente.":
   'Prices are shown in euros, all taxes included. Pre-owned watches fall under the special margin scheme: VAT is not shown separately on the invoice and cannot be recovered by the buyer. Delivery costs are extra and are communicated before the sale is concluded.',
 '3. Commande et réservation': '3. Orders and reservations',
 "La vente est conclue en boutique ou à distance (WhatsApp, e-mail, téléphone) par la signature d'un bon de commande qui reprend la montre, le prix, les frais éventuels et les conditions de garantie.":
   'The sale is concluded in the boutique or at a distance (WhatsApp, email, phone) by signing an order form stating the watch, the price, any costs and the warranty terms.',
 "Une montre peut être réservée moyennant le versement d'un acompte dont le montant est fixé d'un commun accord selon la pièce et indiqué sur le bon de commande. La réservation engage les deux parties. Si l'acheteur renonce à l'achat, l'acompte reste acquis à Machiavelli Watches à titre d'indemnité. Si Machiavelli Watches ne peut pas livrer la montre réservée pour une raison qui lui est imputable, elle rembourse l'acompte et verse à l'acheteur une indemnité d'un montant égal. Lorsque la réservation est conclue à distance par un consommateur, l'acompte est remboursé en cas d'exercice du droit de rétractation (article 7).":
   'A watch may be reserved against payment of a deposit, the amount of which is agreed by both parties depending on the piece and stated on the order form. The reservation is binding on both parties. If the buyer withdraws from the purchase, the deposit is retained by Machiavelli Watches as compensation. If Machiavelli Watches cannot deliver the reserved watch for a reason attributable to it, it refunds the deposit and pays the buyer compensation of an equal amount. When the reservation is made at a distance by a consumer, the deposit is refunded if the right of withdrawal is exercised (article 7).',
 '4. Paiement': '4. Payment',
 'Moyens de paiement acceptés : virement bancaire, carte bancaire, Bancontact et espèces. Conformément à la loi belge, un paiement en espèces est limité à 3.000 € par achat ; au-delà, le paiement s\'effectue par virement ou par carte. La montre reste la propriété de Machiavelli Watches jusqu\'au paiement complet du prix.':
   'Accepted payment methods: bank transfer, bank card, Bancontact and cash. In accordance with Belgian law, cash payments are limited to €3,000 per purchase; above that, payment is made by bank transfer or card. The watch remains the property of Machiavelli Watches until the price has been paid in full.',
 '5. Livraison': '5. Delivery',
 "La montre peut être retirée en boutique sur rendez-vous ou envoyée partout en Europe. Les frais d'envoi, communiqués avant la vente, sont à la charge de l'acheteur. Les envois se font par transporteur, avec suivi et assurance couvrant la valeur de la montre. Pour un consommateur, les risques lui sont transférés lorsqu'il prend physiquement possession de la montre. Pour un envoi hors de l'Union européenne, les éventuels droits de douane et taxes d'importation sont à la charge de l'acheteur.":
   'The watch can be collected in the boutique by appointment or shipped anywhere in Europe. Shipping costs, communicated before the sale, are paid by the buyer. Shipments are made by carrier, tracked and insured for the value of the watch. For a consumer, risk passes when they take physical possession of the watch. For shipments outside the European Union, any customs duties and import taxes are paid by the buyer.',
 '6. Garantie': '6. Warranty',
 "Les montres vendues sont des biens d'occasion : la garantie légale de conformité est limitée à 12 mois à compter de la livraison, durée expressément convenue avec l'acheteur avant la vente et mentionnée sur le bon de commande et la facture. Elle couvre les défauts de conformité existant à la livraison ; elle ne couvre pas l'usure normale, les dommages survenus après la livraison (chocs, chutes, contact avec l'eau au-delà de l'étanchéité garantie, ouverture ou réparation par un tiers), ni les défauts signalés à l'acheteur avant la vente.":
   'The watches sold are second-hand goods: the legal guarantee of conformity is limited to 12 months from delivery, a period expressly agreed with the buyer before the sale and stated on the order form and the invoice. It covers lack of conformity existing at delivery; it does not cover normal wear, damage occurring after delivery (impacts, falls, contact with water beyond the guaranteed water resistance, opening or repair by a third party), or defects disclosed to the buyer before the sale.',
 "Une extension de la garantie à 2 ans peut être souscrite au moment de l'achat. Elle est payante ; son prix et son étendue sont fixés selon la montre et précisés par écrit sur le bon de commande. Cette garantie est celle de Machiavelli Watches et ne constitue pas une garantie du fabricant.":
   "An extension of the warranty to 2 years can be taken out at the time of purchase. It is paid; its price and scope depend on the watch and are set out in writing on the order form. This warranty is given by Machiavelli Watches and is not a manufacturer's warranty.",
 '7. Droit de rétractation (vente à distance à un consommateur)': '7. Right of withdrawal (distance sale to a consumer)',
 "Lorsque la vente est conclue entièrement à distance, le consommateur dispose de 14 jours à compter de la réception de la montre pour se rétracter, sans avoir à se justifier. Il nous en informe par une déclaration claire (e-mail ou formulaire ci-dessous) puis renvoie la montre dans les 14 jours, à ses frais, assurée, dans l'état où il l'a reçue, avec sa boîte, ses papiers et accessoires. Nous remboursons tous les paiements reçus, y compris les frais de livraison standard, au plus tard 14 jours après la rétractation, par le même moyen de paiement ; le remboursement peut être différé jusqu'à la réception de la montre. La responsabilité du consommateur peut être engagée en cas de dépréciation résultant d'une manipulation autre que celle nécessaire pour établir la nature et le bon fonctionnement de la montre (par exemple : retrait des films de protection, ajustement du bracelet, port prolongé). Ce droit ne s'applique pas aux ventes conclues en boutique.":
   'When the sale is concluded entirely at a distance, the consumer has 14 days from receipt of the watch to withdraw, without giving any reason. The consumer informs us by a clear statement (email or the form below), then returns the watch within 14 days, at their own cost, insured, in the condition in which it was received, with its box, papers and accessories. We refund all payments received, including standard delivery costs, no later than 14 days after the withdrawal, using the same means of payment; the refund may be withheld until the watch has been received. The consumer may be held liable for any loss in value resulting from handling beyond what is necessary to establish the nature and proper functioning of the watch (for example: removing protective films, adjusting the bracelet, prolonged wear). This right does not apply to sales concluded in the boutique.',
 'Formulaire de rétractation': 'Withdrawal form',
 '(à renvoyer uniquement si vous souhaitez vous rétracter)': '(to be returned only if you wish to withdraw)',
 "À l'attention de Machiavelli Trading SRL, Place des Combattants 11-13, 6852 Paliseul,": 'To Machiavelli Trading SRL, Place des Combattants 11-13, 6852 Paliseul,',
 'Je vous notifie par la présente ma rétractation du contrat portant sur la vente de la montre ci-dessous :': 'I hereby give notice that I withdraw from the contract for the sale of the watch below:',
 'Maison, modèle et référence : …………………': 'Brand, model and reference: …………………',
 'Commandée le / reçue le : …………………': 'Ordered on / received on: …………………',
 'Nom du consommateur : …………………': 'Name of consumer: …………………',
 'Adresse du consommateur : …………………': 'Address of consumer: …………………',
 "Date et signature (uniquement en cas d'envoi sur papier) : …………………": 'Date and signature (only if sent on paper): …………………',
 '8. Rachat': '8. Buyback',
 "Lorsque Machiavelli Watches rachète une montre, le vendeur garantit en être le propriétaire légitime et présente une pièce d'identité ainsi que, si possible, la facture d'origine, la boîte et les papiers. Le prix est fixé après examen et authentification de la montre. Au-delà de 3.000 €, il est payé par virement.":
   'When Machiavelli Watches buys a watch, the seller warrants that they are its rightful owner and presents an identity document and, where possible, the original invoice, box and papers. The price is set after examination and authentication of the watch. Above €3,000, it is paid by bank transfer.',
 '9. Dépôt-vente': '9. Consignment',
 "Un dépôt-vente fait l'objet d'un contrat écrit, signé par le déposant, qui fixe notamment le prix de vente convenu, la commission de Machiavelli Watches (définie selon la montre), la durée du dépôt, les conditions d'assurance et de restitution. Le déposant garantit être le propriétaire légitime de la montre. Le montant revenant au déposant lui est versé après la vente et le paiement complet par l'acheteur.":
   "A consignment is governed by a written contract signed by the consignor, which sets out in particular the agreed sale price, Machiavelli Watches' commission (set per watch), the duration of the consignment, and the insurance and return conditions. The consignor warrants that they are the rightful owner of the watch. The amount due to the consignor is paid after the sale and full payment by the buyer.",
 '10. Réclamations et litiges': '10. Complaints and disputes',
 'Toute réclamation peut être adressée à': 'Any complaint may be sent to',
 'ou par WhatsApp au +32 484 70 91 09 ; nous y répondons dans les meilleurs délais. Les présentes conditions sont soumises au droit belge. À défaut d\'accord amiable, les tribunaux de Liège sont compétents, sans préjudice des règles impératives protégeant les consommateurs, qui peuvent aussi saisir gratuitement le Service de médiation pour le consommateur (':
   'or by WhatsApp to +32 484 70 91 09; we will reply as quickly as possible. These terms are governed by Belgian law. Failing an amicable agreement, the courts of Liège have jurisdiction, without prejudice to the mandatory rules protecting consumers, who may also refer the matter free of charge to the Consumer Mediation Service (',
 'Politique de': 'Privacy',
 'confidentialité.': 'policy.',
 'Cette politique explique quelles données personnelles Machiavelli Watches traite, pourquoi et quels sont vos droits, conformément au Règlement général sur la protection des données (RGPD) et à la loi belge du 30 juillet 2018.':
   'This policy explains which personal data Machiavelli Watches processes, why, and what your rights are, in accordance with the General Data Protection Regulation (GDPR) and the Belgian law of 30 July 2018.',
 'Responsable du traitement': 'Data controller',
 'Machiavelli Trading SRL (Machiavelli Watches), Place des Combattants 11-13, 6852 Paliseul, BCE 1021.229.955. Contact pour toute question relative à vos données :':
   'Machiavelli Trading SRL (Machiavelli Watches), Place des Combattants 11-13, 6852 Paliseul, BCE 1021.229.955. Contact for any question about your data:',
 'Navigation sur le site': 'Browsing the website',
 "Le site n'utilise": 'The website uses',
 'aucun cookie': 'no cookies',
 ', aucun outil de mesure d\'audience, aucune publicité et aucun traceur. Ses polices et ses scripts sont hébergés avec le site : la consultation des pages ne transmet aucune donnée à des tiers.':
   ', no audience measurement tools, no advertising and no trackers. Its fonts and scripts are hosted with the website: viewing the pages sends no data to third parties.',
 "Comme tout hébergeur, GitHub enregistre des journaux techniques (adresse IP, date et page consultée) afin d'assurer la sécurité et le bon fonctionnement du service. GitHub étant établi aux États-Unis, ces données peuvent y être transférées, dans le cadre des garanties prévues par le RGPD (cadre de protection des données UE–États-Unis ou clauses contractuelles types).":
   'Like any host, GitHub records technical logs (IP address, date and page viewed) to ensure the security and proper operation of the service. As GitHub is established in the United States, this data may be transferred there, under the safeguards provided by the GDPR (EU–US Data Privacy Framework or standard contractual clauses).',
 'Quand vous nous contactez': 'When you contact us',
 "Les boutons « Demander », « Prendre rendez-vous », « Proposer ma montre » et « Sourcer ma montre » préparent un message dans WhatsApp : le site lui-même n'enregistre rien. Les informations que vous nous envoyez (nom, numéro de téléphone, description et photos d'une montre, budget…) sont utilisées uniquement pour vous répondre et donner suite à votre demande. Base légale : les mesures précontractuelles prises à votre demande et notre intérêt légitime à répondre aux personnes qui nous écrivent. WhatsApp, Instagram, TikTok et Facebook sont des services de Meta et de TikTok, soumis à leurs propres politiques de confidentialité.":
   'The “Ask”, “Book an appointment”, “Offer my watch” and “Source my watch” buttons prepare a message in WhatsApp: the website itself records nothing. The information you send us (name, phone number, description and photos of a watch, budget…) is used solely to reply to you and follow up on your request. Legal basis: pre-contractual measures taken at your request and our legitimate interest in replying to people who write to us. WhatsApp, Instagram, TikTok and Facebook are services of Meta and TikTok, subject to their own privacy policies.',
 'Clients, vendeurs et dépôt-vente': 'Clients, sellers and consignment',
 "Pour un achat, un rachat ou un dépôt-vente, nous traitons les données nécessaires à la transaction : identité, coordonnées, informations sur la pièce et documents qui l'accompagnent, données de paiement et de facturation. Base légale : l'exécution du contrat et le respect de nos obligations légales (comptables, fiscales et, le cas échéant, de lutte contre le blanchiment d'argent).":
   'For a purchase, buyback or consignment, we process the data needed for the transaction: identity, contact details, information about the piece and its accompanying documents, payment and billing data. Legal basis: performance of the contract and compliance with our legal obligations (accounting, tax and, where applicable, anti-money-laundering).',
 'Durée de conservation': 'Retention period',
 'Les échanges sans suite sont conservés au maximum 12 mois. Les données liées à une transaction sont conservées pendant la durée imposée par la loi, notamment 10 ans pour les documents comptables.':
   'Exchanges that lead to nothing are kept for a maximum of 12 months. Data relating to a transaction is kept for the period required by law, in particular 10 years for accounting documents.',
 'Destinataires': 'Recipients',
 "Vos données ne sont ni vendues ni louées. Elles ne sont communiquées qu'à nos prestataires lorsque c'est nécessaire (comptable, expert en authentification, transporteur) ou aux autorités lorsque la loi l'impose. Pour gérer nos échanges et notre activité, nous utilisons des outils qui peuvent héberger ces données pour notre compte : WhatsApp (Meta), la messagerie iCloud (Apple) et les outils de gestion de Claude (Anthropic), dans le cadre des garanties prévues par le RGPD.":
   'Your data is never sold or rented. It is only shared with our service providers when necessary (accountant, authentication expert, carrier) or with the authorities when required by law. To manage our exchanges and our business, we use tools that may host this data on our behalf: WhatsApp (Meta), iCloud Mail (Apple) and Claude management tools (Anthropic), under the safeguards provided by the GDPR.',
 'Vos droits': 'Your rights',
 'Vous pouvez demander l\'accès à vos données, leur rectification, leur effacement, la limitation du traitement, vous opposer au traitement, demander la portabilité de vos données et retirer à tout moment un consentement donné. Écrivez-nous à':
   'You can request access to your data, its rectification or erasure, restriction of processing, object to processing, request data portability and withdraw any consent given at any time. Write to us at',
 "ou sur WhatsApp ; nous répondons dans un délai d'un mois.": 'or on WhatsApp; we reply within one month.',
 'Vous pouvez aussi introduire une réclamation auprès de l\'Autorité de protection des données, rue de la Presse 35, 1000 Bruxelles (':
   'You may also lodge a complaint with the Belgian Data Protection Authority, rue de la Presse 35, 1000 Brussels (',
 'Modifications': 'Changes',
 'Cette politique peut être mise à jour, par exemple si de nouveaux services sont ajoutés au site. La date de dernière mise à jour figure en haut de la page.':
   'This policy may be updated, for example if new services are added to the website. The date of the last update is shown at the top of the page.',
}

# ---------- attributs ----------
A = {
 'Machiavelli Watches, haut de page': 'Machiavelli Watches, top of page',
 'Navigation principale': 'Main navigation',
 'Nos engagements': 'Our commitments',
 "Retour à l'accueil": 'Back to home',
 'Filtrer par maison': 'Filter by brand',
 'Chercher un modèle, une référence': 'Search a model or reference',
 'Marque et modèle': 'Brand and model',
 'AAAA': 'YYYY',
 'Marque, modèle, référence': 'Brand, model, reference',
}

# manifeste (texte découpé mot à mot par le script : les *…* marquent les mots lumineux)
MANIFESTE = (
 'Basé à Liège, Machiavelli achète, sélectionne et revend des montres *exclusives* pour des collectionneurs du monde entier. Nous ne fabriquons pas de montres : nous choisissons les *plus belles pièces* des grandes maisons.',
 'Based in Liège, Machiavelli buys, selects and resells *exclusive* watches for collectors around the world. We do not make watches: we choose the *finest pieces* from the great houses.')

# ---------- textes générés par le script ----------
J = [
 ("'Réf. à préciser'", "'Ref. to be confirmed'"),
 ("'Réservée'", "'Reserved'"),
 ('<span class="reserved">Réservée</span>', '<span class="reserved">Reserved</span>'),
 (', voir la fiche"', ', view details"'),
 ("Aucune montre ne correspond. Essayez une autre maison ou un autre mot.", 'No watch matches. Try another brand or another word.'),
 ("aria-pressed=\"${b === brand}\">${esc(b)}</button>", "aria-pressed=\"${b === brand}\">${esc(b === 'Toutes' ? 'All' : b)}</button>"),
 ("Partager cette montre", 'Share this watch'),
 ("'Lien copié ✓'", "'Link copied ✓'"),
 ("Copier le lien", 'Copy link'),
 ('role="menuitem">E-mail</a>', 'role="menuitem">Email</a>'),
 ('class="sh-close" role="menuitem">Fermer</button>', 'class="sh-close" role="menuitem">Close</button>'),
 ("' · réf. '", "' · ref. '"),
 ("euro(w.price) + ' TTC'} chez Machiavelli Watches", "euro(w.price) + ' incl. VAT'} at Machiavelli Watches"),
 ("Bonjour, je suis intéressé par la ${w.brand} ${w.model}${w.ref ? ' (réf. ' + w.ref + ')' : ''}.", "Hello, I am interested in the ${w.brand} ${w.model}${w.ref ? ' (ref. ' + w.ref + ')' : ''}."),
 ("Bonjour, je souhaite prendre rendez-vous pour voir la ${w.brand} ${w.model}${w.ref ? ' (réf. ' + w.ref + ')' : ''}.", "Hello, I would like to book an appointment to see the ${w.brand} ${w.model}${w.ref ? ' (ref. ' + w.ref + ')' : ''}."),
 ('aria-label="Photo précédente"', 'aria-label="Previous photo"'),
 ('aria-label="Photo suivante"', 'aria-label="Next photo"'),
 ("'Vue de face · photo réelle à venir'", "'Front view · real photo coming soon'"),
 ('aria-label="Photos de la montre"', 'aria-label="Watch photos"'),
 ('<span class="kicker">Vidéo de la pièce</span>', '<span class="kicker">Video of the piece</span>'),
 ("const VIEWS = ['Face', 'Trois-quarts', 'Cadran', 'Profil'];", "const VIEWS = ['Front', 'Three-quarter', 'Dial', 'Side'];"),
 ("`Vue ${VIEWS[gv].toLowerCase()} · photo réelle à venir`", "`${VIEWS[gv]} view · real photo coming soon`"),
 ("Réf. ${esc(w.ref || 'à préciser')}", "Ref. ${esc(w.ref || 'to be confirmed')}"),
 ('<span class="ttc">TTC</span>', '<span class="ttc">incl. VAT</span>'),
 ("Être prévenu d'une pièce similaire", 'Get notified of a similar piece'),
 ('Demander sur WhatsApp', 'Ask on WhatsApp'),
 ('rel="noopener">Prendre rendez-vous</a>', 'rel="noopener">Book an appointment</a>'),
 ('<dt>Maison</dt>', '<dt>Brand</dt>'),
 ('<dt>Modèle</dt>', '<dt>Model</dt>'),
 ('<dt>Référence</dt>', '<dt>Reference</dt>'),
 ("esc(w.ref || 'À préciser')", "esc(w.ref || 'To be confirmed')"),
 ('<dt>Année</dt>', '<dt>Year</dt>'),
 ('<dt>Boîte &amp; papiers</dt>', '<dt>Box &amp; papers</dt>'),
 ('<dt>État</dt>', '<dt>Condition</dt>'),
 ('<li>Authentifiée par un expert</li>', '<li>Authenticated by an expert</li>'),
 ('<li>Garantie 1 an, extensible à 2 ans</li>', '<li>1-year warranty, extendable to 2 years</li>'),
 ('<li>Disponible immédiatement</li>', '<li>Available immediately</li>'),
 ('data-share="${esc(w.id)}">Partager <svg', 'data-share="${esc(w.id)}">Share <svg'),
 ('Illustration en attendant les photos réelles de la pièce.', 'Illustration pending real photos of the piece.'),
 ("etat: ['Neuve', 'Comme neuve', 'Très bon état', 'Bon état', 'État d’usage'],", "etat: ['New', 'Like new', 'Very good condition', 'Good condition', 'Signs of wear'],"),
 ("fullset: ['Full set (boîte et papiers)', 'Boîte seulement', 'Papiers seulement', 'Montre seule'],", "fullset: ['Full set (box and papers)', 'Box only', 'Papers only', 'Watch only'],"),
 ('selected disabled>Choisir</option>', 'selected disabled>Choose</option>'),
 ("kind === 'sell' ? 'Vendre votre montre' : 'Sourcer votre montre'", "kind === 'sell' ? 'Sell your watch' : 'Source your watch'"),
 ('Ajoutez les 3 photos et complétez les champs soulignés.', 'Add the 3 photos and complete the underlined fields.'),
 ("'Complétez les champs soulignés.'", "'Complete the underlined fields.'"),
 ("'*PROPOSITION DE VENTE*', '_Machiavelli Watches · formulaire du site_'", "'*SALE OFFER*', '_Machiavelli Watches · website form (EN)_'"),
 ("'*LA MONTRE*', `• Modèle : ${v('nom')}`, `• Référence : ${v('ref')}`, `• Année : ${v('annee')}`, `• État : ${v('etat')}`, `• Full set : ${v('fullset')}`",
  "'*THE WATCH*', `• Model: ${v('nom')}`, `• Reference: ${v('ref')}`, `• Year: ${v('annee')}`, `• Condition: ${v('etat')}`, `• Full set: ${v('fullset')}`"),
 ("'*LA DEMANDE*', `• Formule : ${v('formule')}`, `• Prix désiré : ${eur(v('prix'))}`", "'*THE REQUEST*', `• Option: ${v('formule')}`, `• Desired price: ${eur(v('prix'))}`"),
 ("'*LE CLIENT*', `• Nom : ${v('client')}`, `• Contact : ${v('contact')}`", "'*THE CLIENT*', `• Name: ${v('client')}`, `• Contact: ${v('contact')}`"),
 ("'_3 photos de la montre jointes à ce message._'", "'_3 photos of the watch attached to this message._'"),
 ("'*DEMANDE DE SOURCING*', '_Machiavelli Watches · formulaire du site_'", "'*SOURCING REQUEST*', '_Machiavelli Watches · website form (EN)_'"),
 ("'*LA MONTRE RECHERCHÉE*', `• Référence : ${v('ref')}`, `• Année : ${v('annee') || 'indifférente'}`, `• Budget maximum : ${eur(v('prix'))}`",
  "'*THE WATCH WANTED*', `• Reference: ${v('ref')}`, `• Year: ${v('annee') || 'any'}`, `• Maximum budget: ${eur(v('prix'))}`"),
 ("'*LE CLIENT*', `• Nom : ${v('client')}`, `• Téléphone : ${v('tel')}`, `• E-mail : ${v('email')}`", "'*THE CLIENT*', `• Name: ${v('client')}`, `• Phone: ${v('tel')}`, `• Email: ${v('email')}`"),
 ("'Votre proposition s’est ouverte dans WhatsApp. Ajoutez-y vos 3 photos, puis envoyez : nous vous répondons au plus vite.'",
  "'Your offer has opened in WhatsApp. Add your 3 photos, then send it: we will reply as soon as possible.'"),
 ("'Votre demande s’est ouverte dans WhatsApp. Envoyez-la : nous lançons la recherche et revenons vers vous.'",
  "'Your request has opened in WhatsApp. Send it: we will start the search and get back to you.'"),
 ("b.textContent = 'Copié'; setTimeout(() => (b.textContent = 'Copier'), 1600);", "b.textContent = 'Copied'; setTimeout(() => (b.textContent = 'Copy'), 1600);"),
 # données du stock (valeurs en français dans la base) → anglais à l'affichage
 ("  function setStock(list) {\n", "  function setStock(list) {\n    list = list.map(enWatch);\n"),
]

EN_DATA = r'''
  // ---------- version anglaise : traduction des valeurs du stock ----------
  const EN_VAL = { 'Très bon état': 'Very good condition', 'Bon état': 'Good condition', 'État d’usage': 'Signs of wear', "État d'usage": 'Signs of wear',
    'Neuve': 'New', 'Neuf': 'New', 'Comme neuve': 'Like new', 'Excellent état': 'Excellent condition',
    'Full set (boîte et papiers)': 'Full set (box and papers)', 'Boîte seulement': 'Box only', 'Papiers seulement': 'Papers only', 'Montre seule': 'Watch only',
    'Non communiquée': 'Not disclosed', 'Non communiqué': 'Not disclosed' };
  const EN_MONTHS = { 'Janvier': 'January', 'Février': 'February', 'Mars': 'March', 'Avril': 'April', 'Mai': 'May', 'Juin': 'June', 'Juillet': 'July', 'Août': 'August', 'Septembre': 'September', 'Octobre': 'October', 'Novembre': 'November', 'Décembre': 'December' };
  const enVal = (v) => { if (typeof v !== 'string') return v; const t = v.trim(); if (EN_VAL[t]) return EN_VAL[t]; return t.replace(/^(\p{L}+)(?=\s+\d{4}$)/u, (m) => EN_MONTHS[m[0].toUpperCase() + m.slice(1).toLowerCase()] || m); };
  const enWatch = (w) => ({ ...w, model: String(w.model || '').replace(/édition limitée (\d+) pièces/i, 'limited edition of $1 pieces'), year: enVal(w.year), set: enVal(w.set), cond: enVal(w.cond) });
'''

LANG_FR = '<a href="en.html" class="lang-sw" lang="en" hreflang="en"><span class="k">EN</span>English</a>'
LANG_EN = '<a href="./" class="lang-sw" lang="fr" hreflang="fr"><span class="k">FR</span>Français</a>'


def norm(s):
    return ' '.join(s.split())


def main():
    s = open(SRC, encoding='utf-8').read()
    miss = []
    used_t, used_a = set(), set()

    # 1. scripts : remplacements exacts
    for old, new in J:
        if old not in s:
            miss.append('JS  ' + old[:90]); continue
        s = s.replace(old, new)
    if 'function setStock(list) {\n    list = list.map(enWatch);' in s:
        s = s.replace('  const STATIC = true;', EN_DATA + '  const STATIC = true;', 1)
    if MANIFESTE[0] in s: s = s.replace(MANIFESTE[0], MANIFESTE[1])
    else: miss.append('MANIFESTE')

    # 2. HTML hors scripts / styles : nœuds texte et attributs
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->)', s, flags=re.S)
    for i in range(0, len(parts), 2):
        seg = parts[i]
        def tx(m):
            raw = m.group(1); key = norm(raw)
            if key in T:
                used_t.add(key)
                lead = raw[:len(raw) - len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
                return '>' + lead + T[key] + trail + '<'
            return m.group(0)
        seg = re.sub(r'>([^<>]+)<', tx, seg)
        def at(m):
            v = m.group(2)
            if v in A: used_a.add(v); return f'{m.group(1)}="{A[v]}"'
            return m.group(0)
        seg = re.sub(r'\b(placeholder|aria-label|title|alt)="([^"]+)"', at, seg)
        parts[i] = seg
    s = ''.join(parts)

    # 3. WhatsApp pré-rempli (entretien)
    old_q = urllib.parse.quote('Bonjour, je souhaite des informations sur l’entretien de ma montre.', safe='')
    s = s.replace(old_q, urllib.parse.quote('Hello, I would like information about servicing my watch.', safe=''))

    # 4. en-tête, langue, sélecteur
    s = s.replace('<html lang="fr"', '<html lang="en"', 1)
    s = s.replace('Machiavelli Watches — Montres de luxe d\'occasion à Liège', 'Machiavelli Watches — Pre-owned luxury watches in Liège')
    s = s.replace("Machiavelli Watches, Liège : vente, rachat, dépôt-vente et sourcing de montres de luxe d'occasion. Chaque pièce est authentifiée par un expert.",
                  'Machiavelli Watches, Liège: sale, buyback, consignment and sourcing of pre-owned luxury watches. Every piece is authenticated by an expert.')
    s = s.replace('Vente, rachat, dépôt-vente et sourcing de montres de luxe. Chaque pièce authentifiée par un expert.',
                  'Sale, buyback, consignment and sourcing of luxury watches. Every piece authenticated by an expert.')
    s = s.replace('content="fr_BE"', 'content="en_GB"')
    s = re.sub(r'(<link rel="canonical" href="[^"]*?/)(")', r'\1en.html\2', s, count=1)
    s = re.sub(r'(<meta property="og:url" content="[^"]*?/)(")', r'\1en.html\2', s, count=1)
    n_sw = s.count(LANG_FR)
    s = s.replace(LANG_FR, LANG_EN)
    if n_sw == 0: miss.append('LANG switch')

    for k in T:
        if k not in used_t: miss.append('TXT ' + k[:90])
    for k in A:
        if k not in used_a: miss.append('ATTR ' + k)

    open(DST, 'w', encoding='utf-8').write(s)
    print(f'en.html écrit ({len(s)} octets).')
    if miss:
        print('À vérifier — textes non retrouvés :'); [print('  -', m) for m in miss]


if __name__ == '__main__':
    main()
