import QuoteList from "../quotes/QuoteList"
import Sidebar from "./Sidebar"

const RightSidebar = () => {
  return (
	<Sidebar>
		<div className="space-y-4">
			<p className="text-sm text-gray-500">Source sitée</p>
			<QuoteList/>
		</div>
	</Sidebar>
  )
}

export default RightSidebar
