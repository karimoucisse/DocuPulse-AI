
const ImportItem = ({name, type}) => {
  return (
	<div className="flex justify-between items-center border-l-3 border-primary px-4 py-2">
		<p className="text-sm">{name}</p>
		<p className="text-xs text-gray-400">{type.toUpperCase()}</p>
	</div>
  )
}

export default ImportItem
