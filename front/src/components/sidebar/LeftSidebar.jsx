import ImportList from "../import/ImportList"
import Logo from "../Logo"
import Sidebar from "./Sidebar"

const LeftSidebar = () => {
  return (
	<Sidebar>
		<div className="space-y-4">
			<Logo/>
			<button className="btn bg-primary btn-sm w-full">+ Importer un document</button>
			<ImportList/>
		</div>
	</Sidebar>
  )
}

export default LeftSidebar
