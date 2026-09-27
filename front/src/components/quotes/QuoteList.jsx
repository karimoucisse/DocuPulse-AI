import QuoteItem from "./QuoteItem"

const QuoteList = () => {
  return (
	  <div className="space-y-4">
      <QuoteItem  file_name="contrat_prestation.pdf" page_number="4"
        quote="Toute résiliation devra être notifiée par écrit avec un préavis de
        30 jours ouvrés, sauf cas de faute grave dûment justifié."/>
      <QuoteItem  file_name="contrat_prestation.pdf" page_number="4"
      quote="Toute résiliation devra être notifiée par écrit avec un préavis de
      30 jours ouvrés, sauf cas de faute grave dûment justifié."/>
    </div>
  )
}

export default QuoteList
