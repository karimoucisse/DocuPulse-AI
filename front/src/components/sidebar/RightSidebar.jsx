import QuoteList from "../quotes/QuoteList"
import Sidebar from "./Sidebar"

const RightSidebar = ({sources}) => {
	console.log(sources)
  return (
	<Sidebar>
		<div className="space-y-4">
			<p className="text-sm text-gray-500">Source sitée</p>
			<QuoteList sources={sources}/>
		</div>
	</Sidebar>
  )
}

export default RightSidebar
