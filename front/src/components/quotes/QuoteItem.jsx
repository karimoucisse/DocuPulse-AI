
const QuoteItem = ({file_name, page_number, quote }) => {
  return (
	  <div className="space-y-2 p-2 shadow-xs">
      <p className="text-sm font-bold">{file_name}</p>
      <p className="text-xs text-primary">Page {page_number}</p>
      <div className="flex flex-wrap border-l-4 border-amber-300 bg-amber-300/10 p-4">
        <p className="text-sm italic">{"<<"} {quote} {">>"}</p>
      </div>
      <div className="space-x-2">
        <button className="border border-gray-600 text-xs px-2 py-1 rounded-sm cursor-pointer hover:border-primary">Voir la Page</button>
        <button className="border border-gray-600 text-xs px-2 py-1 rounded-sm cursor-pointer hover:border-primary">Copier</button>
      </div>
    </div>
  )
}

export default QuoteItem
