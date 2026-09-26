import ImportList from "../import/ImportList"
import Sidebar from "./Sidebar"

const LeftSidebar = () => {
  return (
	<Sidebar>
		<div className="space-y-4">
			<p className="text-lg">Docu<span className="text-primary">Pulse</span></p>
			<button className="btn bg-primary btn-sm w-full">+ Importer un document</button>
			<ImportList/>
		</div>
	</Sidebar>
  )
}

export default LeftSidebar
